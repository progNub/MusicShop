from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from catalog.views import CategoryListView, CatalogItemListView, CreateCatalogItemView, DeleteCatalogItemView, \
    UpdateCatalogItemView

urlpatterns = [
    path("<slug:slug>", CategoryListView.as_view(), name="category"),
    path('items/', CatalogItemListView.as_view(), name='catalog_item_list'),
    path("add/item/", CreateCatalogItemView.as_view(), name="add_catalog_item"),
    path("update/item/", UpdateCatalogItemView.as_view(), name="update_catalog_item"),
    path("delete/item/<slug:slug>", DeleteCatalogItemView.as_view(), name="delete_catalog_item"),
]
