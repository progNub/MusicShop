from django.contrib.auth import login, logout

from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import UserRegisterForm, UserAuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import get_user_model
from accounts.task import send_message_to_confirm_email
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

User = get_user_model()


# Create your views here.


class ShowProfileUser(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile_user.html'
    context_object_name = 'user'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/auth/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        domain = self.request.META['HTTP_HOST']
        token = default_token_generator.make_token(user)
        send_message_to_confirm_email.delay(domain=domain, user_id=user.id, token=token)
        messages.info(self.request,
                      "Вы успешно зарегистрировались. На ваш email отправлено письмо, с инструкцией подтверждения")
        return response


def confirm_email(request, uidb64, token):
    user_id = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, id=user_id)
    if user.is_confirmed_email:
        messages.warning(request, 'Ваш email уже подтвержден.')
        return redirect(reverse_lazy('home'))

    if default_token_generator.check_token(user, token):
        user.is_confirmed_email = True
        user.save()
        login(request, user)
        messages.success(request, 'Ваш email успешно подтвержден.')
        return redirect(reverse_lazy('home'))
    messages.error(request, 'Неверный токен.')
    return redirect(reverse_lazy('home'))


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/auth/login.html'
    form_class = UserAuthenticationForm
    next_page = reverse_lazy('home')


def user_logout(request: HttpRequest):
    logout(request)
    return redirect('home')
