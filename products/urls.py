from django.urls import path

from products.views import DetailProduct, CreateProduct, UpdateProduct

urlpatterns = [
    path('create/', CreateProduct.as_view(), name='create_product'),
    path('update/<slug:slug>', UpdateProduct.as_view(), name='update_product'),
    path('<slug:product_slug>/', DetailProduct.as_view(), name='show-product'),
]
