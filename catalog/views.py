from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View

from catalog import forms
from catalog.models import CatalogItem
from django.urls import reverse_lazy
from django.db.models import F
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import OuterRef, Subquery

from characteristic.mixin import StaffOrSuperuserRequiredMixin
from products.views import Home


# Create your views here.


class CategoryListView(Home):
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super(CategoryListView, self).get_queryset()
        slug = self.kwargs.get('slug')
        queryset = queryset.filter(category__slug=slug)
        return queryset


class CatalogItemListView(ListView):
    model = CatalogItem
    template_name = 'catalog/list_catalog_item.html'
    context_object_name = 'catalog_item_list'
    form_class = forms.CatalogItemForm
    success_url = reverse_lazy('catalog_item_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get_queryset(self):
        queryset = self.model.get_tree_items()
        return queryset


class CreateCatalogItemView(CreateView):
    model = CatalogItem
    form_class = forms.CatalogItemForm
    template_name = 'catalog/list_catalog_item.html'
    success_url = reverse_lazy('catalog_item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.CatalogItemForm(self.request.POST)
        context['catalog_item_list'] = self.model.get_tree_items()
        return context


class UpdateCatalogItemView(View):
    model = CatalogItem
    form_class = forms.UpdateCatalogItemForm
    success_url = reverse_lazy('catalog_item_list')

    def get_context_data(self, **kwargs):
        context = {'form': self.form_class(self.request.POST),
                   'catalog_item_list': self.model.get_tree_items()}
        return context

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            response = render(self.request, 'catalog/list_catalog_item.html', context=self.get_context_data())
        return response


class DeleteCatalogItemView(DeleteView):
    model = CatalogItem
    success_url = reverse_lazy('catalog_item_list')
