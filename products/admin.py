from django.contrib import admin
from products.models import Product, Category, Brand, ProductImage, SubCategory


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('id', 'name', 'category', 'description', 'price', 'availability', 'count_images', 'brand')
    list_display_links = ('id', 'name')

    def count_images(self, obj: Product):
        return obj.images.count()


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('id', 'name', 'count_sub_categories')
    list_display_links = ('id', 'name')

    def count_sub_categories(self, obj: Product):
        return obj.sub_category.count()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
