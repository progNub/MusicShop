from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя:',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'RegisterInputUsername',
                                                             'placeholder': 'Введите имя пользователя'}))

    firstname = forms.CharField(label='Имя:', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'id': 'RegisterInputFirstname',
                                                              'placeholder': 'Введите Имя'}))

    lastname = forms.CharField(label='Фамилия:', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'RegisterInputLastname',
                                                             'placeholder': 'Введите Фамилию'}))

    email = forms.EmailField(label='Адрес электронной почты:',
                             widget=forms.EmailInput(attrs={'name': 'email',
                                                            'class': 'form-control',
                                                            'id': 'RegisterInputEmail1',
                                                            'placeholder': 'Введите адрес электронной почты'}))

    password1 = forms.CharField(label='Пароль:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': 'RegisterInputPassword1',
                                                                  'placeholder': 'Введите пароль'}))

    password2 = forms.CharField(label='Повторите пароль:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': 'RegisterInputPassword2',
                                                                  'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'email', 'password1', 'password2')


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя:',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loginInputUsername',
                                                             'placeholder': 'Введите имя пользователя',
                                                             'autofocus': True}))
    password = forms.CharField(label='Пароль:',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'id': 'loginInputPassword1',
                                                                 'placeholder': 'Введите пароль'}))


