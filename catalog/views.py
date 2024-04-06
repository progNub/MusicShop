from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import CatalogItem
from common_models.models import ProductSubFeature
from products.models import Product, ProductImage
from django.db.models import F
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.db.models import OuterRef, Subquery

from products.views import Home


# Create your views here.


class CatalogListView(Home):

    def get_queryset(self):
        queryset = super(CatalogListView, self).get_queryset()
        slug = self.kwargs.get('category_slug')
        queryset = queryset.filter(category__slug=slug)
        return queryset
