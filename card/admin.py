from django.contrib import admin

from card.models import Order


# Register your models here.



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

