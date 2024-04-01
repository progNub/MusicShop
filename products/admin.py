from django.contrib import admin
from products.models import Product, Category, Brand, ProductImage, Feature, ProductFeature
from django.db import models


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductFeatureInline]
    list_display = ('id', 'name', 'category', 'description', 'price', 'availability', 'count_images', 'brand')
    list_display_links = ('id', 'name')

    def count_images(self, obj: Product):
        return obj.images.count()


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    list_display = ('id', 'name', 'parent_category')
    list_display_links = ('id', 'name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent_category':
            kwargs['queryset'] = Category.objects.exclude(id=request.resolver_match.kwargs.get('object_id'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('products', 'features', 'value')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass
