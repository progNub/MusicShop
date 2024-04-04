import os
import uuid
from slugify import slugify
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = 'category_product'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}{self.name}'


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='Категория', related_name='sub_category')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        slug = self.category.name + '_' + self.name
        print(slug)
        self.slug = slugify(slug)
        super(SubCategory, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sub_category_product'
        unique_together = ('name', 'category',)

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
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Производитель',
                              related_name='products')
    features = models.ManyToManyField('SubFeature', through='ProductSubFeature', )
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return f'product/{self.slug}'

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


class Feature(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Feature, self).save(*args, **kwargs)


class SubFeature(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='sub_feature', null=False)
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('name', 'feature')

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.name}:{self.feature.name}>'

    def save(self, *args, **kwargs):
        slug = self.feature.name + '_' + self.name
        self.slug = slugify(slug)
        super(SubFeature, self).save(*args, **kwargs)


class ProductSubFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sub_feature = models.ForeignKey(SubFeature, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'feature_product'
        unique_together = ('product', 'sub_feature')

    def __str__(self):
        return f"{self.product.name} - {self.sub_feature.name}: {self.value}"

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.product.name}:{self.sub_feature.name}:{self.value}>'
