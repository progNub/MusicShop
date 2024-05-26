from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Номер телефона")
    is_confirmed_email = models.BooleanField(default=False, blank=True, null=False, verbose_name="статус email")

    class Meta:
        db_table = 'user'


class AddressUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    home = models.CharField(max_length=100, null=True, blank=True, verbose_name='Дом')
    street = models.CharField(max_length=100, null=True, blank=True, verbose_name='Улица')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')

    def __str__(self):
        return f"{self.user.username} - {self.home} {self.street} {self.city}"
