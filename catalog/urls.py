from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from catalog.views import CatalogListView

urlpatterns = [
    path("<slug:category_slug>", CatalogListView.as_view(), name="category"),

]
