# Generated by Django 5.0.3 on 2024-05-12 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Ожидает обработки'), ('processing', 'В обработке'), ('shipped', 'Отправлен'), ('completed', 'Завершен'), ('cancelled', 'Отменен')], default=None, max_length=50, null=True),
        ),
    ]