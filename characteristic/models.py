from django.db import models
from slugify import slugify


# Create your models here.

class Feature(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристика"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Feature, self).save(*args, **kwargs)


class SubFeature(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='sub_feature', null=False,
                                verbose_name='Характеристика')
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('name', 'feature')
        verbose_name = "Подхарактеристика"
        verbose_name_plural = "Подхарактеристика"

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.name}:{self.feature.name}>'

    def save(self, *args, **kwargs):
        slug = self.feature.name + '-' + self.name
        self.slug = slugify(slug)
        super(SubFeature, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'brand_product'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}{self.name}'
