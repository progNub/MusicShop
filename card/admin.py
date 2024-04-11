from django.contrib import admin

from card.models import Order, Deliveryman


# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'date', 'payment_status', 'status',)


@admin.register(Deliveryman)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone')
