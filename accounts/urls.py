from django.urls import path

from accounts.views import RegisterUser, MyLoginView, user_logout, ShowProfileUser, confirm_email

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('confirm/email/<uidb64>/<token>', confirm_email, name='registration-confirm-email'),
    path('profile/<str:username>', ShowProfileUser.as_view(), name='profile'),
]
