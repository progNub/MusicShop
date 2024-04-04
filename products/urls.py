from django.urls import path

from products.views import DetailProduct

urlpatterns = [
    path('<slug:product_slug>/', DetailProduct.as_view(), name='show-product'),
]
