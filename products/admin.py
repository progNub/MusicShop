from django.contrib import admin
from products.models import Product, Category, Brand, ProductImage, Feature, ProductFeature, SubCategory


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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('brand', 'category')
        queryset = queryset.prefetch_related('images', 'features')
        return queryset


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name')
    exclude = ('slug',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('category')
        return queryset


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    exclude = ('slug',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    exclude = ('slug',)


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
