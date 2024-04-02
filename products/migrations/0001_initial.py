# Generated by Django 5.0.3 on 2024-03-30 17:34

import django.db.models.deletion
import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'brand_product',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category')),
            ],
            options={
                'db_table': 'category_product',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена')),
                ('availability', models.BooleanField(default=True, verbose_name='Наличие')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.brand', verbose_name='Производитель')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category', verbose_name='Категория')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('features', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.feature')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'feature_product',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.ManyToManyField(through='products.ProductFeature', to='products.feature'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.product_image_upload)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'db_table': 'image_product',
            },
        ),
    ]
