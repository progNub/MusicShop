from django.urls import path

from card.views import OrderListView, AddProductToCartView, RemoveProductToCartView, UpdateProductQuantityInView

urlpatterns = [
    path("", OrderListView.as_view(), name="orders"),  # главная страница.
    path('add/<slug:product_slug>', AddProductToCartView.as_view(), name='add_product_to_card'),
    path('remove/<int:order_id>', RemoveProductToCartView.as_view(), name='remove_product_from_card'),
    path('update-quantity/', UpdateProductQuantityInView.as_view(), name='update_order_product_quantity'),
]
