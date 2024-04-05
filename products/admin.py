from django.contrib import admin
from common_models.models import ProductSubFeature
from products.models import Product, ProductImage


# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSubFeatureInline(admin.TabularInline):
    model = ProductSubFeature
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSubFeatureInline]
    list_display = (
        'id', 'name', 'category', 'description', 'price', 'availability', 'count_images', 'brand')
    list_display_links = ('id', 'name')
    exclude = ('slug',)

    def count_images(self, obj: Product):
        return obj.images.count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('brand', 'category')
        queryset = queryset.prefetch_related('images', 'features')
        return queryset
