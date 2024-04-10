from django.urls import path

from products.views import DetailProduct, CreateProduct

urlpatterns = [
    path('create/', CreateProduct.as_view(), name='create_product'),
    path('<slug:product_slug>/', DetailProduct.as_view(), name='show-product'),
]
