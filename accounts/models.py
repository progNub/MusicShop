from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'user'



