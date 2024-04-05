from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from common_models.models import ProductSubFeature


# Register your models here.
@admin.register(ProductSubFeature)
class ProductSubFeatureAdmin(admin.ModelAdmin):
    list_display = ('product_link', 'sub_feature', 'value')


    def product_link(self, obj):
        link = reverse("admin:products_product_change", args=[obj.product.id])  # app_name:model_name_change
        return format_html('<a href="{}">{}</a>', link, obj.product)

    product_link.short_description = 'Product'  # Название колонки в админке
