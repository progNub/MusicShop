from django.contrib import admin
from products.models import Product, Category, Brand, ProductImage, Feature, ProductFeature, SubCategory
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


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name')
    list_editable = ('category',)


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


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
