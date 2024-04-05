from django.contrib import admin

from characteristic.models import Brand, SubFeature, Feature
from common_models.models import ProductSubFeature
from products.models import Product

# Register your models here.

from django.db.models import Count


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count_products')
    list_display_links = ('id', 'name')
    exclude = ('slug',)

    def get_queryset(self, request):
        # Аннотируем каждый объект Brand количеством связанных продуктов
        queryset = super().get_queryset(request).annotate(
            count_products=Count('products')
        )
        return queryset

    def count_products(self, obj: Brand):
        # Возвращаем аннотированное значение
        return obj.count_products


@admin.register(SubFeature)
class SubFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'feature', 'count_products')
    exclude = ('slug',)

    @staticmethod
    def count_products(obj: SubFeature):
        return obj.count_products

    def get_queryset(self, request):
        # Аннотируем каждый объект Brand количеством связанных продуктов
        queryset = super().get_queryset(request).annotate(
            count_products=Count('productsubfeature')
        )
        return queryset


class SubFeatureInline(admin.TabularInline):
    model = SubFeature
    extra = 1
    exclude = ('slug',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    inlines = [SubFeatureInline]
    list_display = ('name', 'count_sub_features',)
    exclude = ('slug',)

    @staticmethod
    def count_sub_features(obj: Feature):
        return SubFeature.objects.filter(feature_id=obj.id).count()
