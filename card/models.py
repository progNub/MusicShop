from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

User = get_user_model()


# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True, default=None)
    delivery = models.ForeignKey('Deliveryman', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    address = models.ForeignKey('accounts.AddressUser', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Адрес доставки')

    class Meta:
        db_table = 'order'
        unique_together = ('user', 'product')
        ordering = ('-date',)
        indexes = [
            models.Index(fields=['user', 'product']),
        ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def total_price(self):
        return int(self.quantity) * self.product.price

    @staticmethod
    def add_product_to_cart(user, product_slug, quantity=1):
        product = Product.objects.filter(slug=product_slug).first()
        if product:
            order, created = Order.objects.get_or_create(user=user, product=product,
                                                         defaults={'quantity': quantity})

            if not created:
                order.quantity = quantity
                order.save()
            return order

    def set_quantity(self, quantity):
        self.quantity = quantity
        self.save()
        return self.quantity

    def __str__(self):
        return f'{self.user} - {self.product} - {self.quantity}'

    def __repr__(self):
        return f'{self.__class__.__name__}{self.user} - {self.product} - {self.quantity}'


class Deliveryman(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    class Meta:
        db_table = 'delivery'
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
