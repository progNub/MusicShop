from django.urls import path

from accounts.views import RegisterUser, MyLoginView, user_logout

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
]
