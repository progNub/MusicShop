import os
import uuid
from slugify import slugify
from django.db import models
from django.urls import reverse


from catalog.models import CatalogItem
from characteristic.models import Brand, SubFeature


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    category = models.ForeignKey(CatalogItem, on_delete=models.SET_NULL, verbose_name='Категория',
                                 related_name='products', null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Производитель',
                              related_name='products')
    features = models.ManyToManyField(SubFeature, through='common_models.ProductSubFeature')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('show-product', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

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
