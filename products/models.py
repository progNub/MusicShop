import os
import uuid

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'category_product'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}{self.name}'


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'brand_product'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Производитель')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    availability = models.BooleanField(default=True, verbose_name='Наличие')

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}{self.name}'


def product_image_upload(instance, filename):
    # Получение имени файла и расширения
    base_filename, extension = os.path.splitext(filename)

    # Генерация уникального имени для файла изображения
    unique_filename = f'{uuid.uuid4()}-{base_filename}{extension}'
    return f'product_images/{unique_filename}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_image_upload)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'image_product'

    def __str__(self):
        return f'{str(self.image)}'

    def __repr__(self):
        return f'{self.__class__.__name__}{str(self.image)}'
