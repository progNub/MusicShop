from django.contrib.auth import login, logout

from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import UserRegisterForm, UserAuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import get_user_model

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
        login(self.request, user)
        return response


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/auth/login.html'
    form_class = UserAuthenticationForm
    next_page = reverse_lazy('home')


def user_logout(request: HttpRequest):
    logout(request)
    return redirect('home')
