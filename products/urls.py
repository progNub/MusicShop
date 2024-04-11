from django.urls import path

from products.views import DetailProduct, CreateProduct, UpdateProduct, DeleteProduct

urlpatterns = [
    path('create/', CreateProduct.as_view(), name='create_product'),
    path('<slug:slug>/', DetailProduct.as_view(), name='show-product'),
    path('update/<slug:slug>', UpdateProduct.as_view(), name='update_product'),
    path('delete/<slug:slug>/', DeleteProduct.as_view(), name='delete-product'),
]
