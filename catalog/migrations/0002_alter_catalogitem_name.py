# Generated by Django 5.0.3 on 2024-05-12 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogitem',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]