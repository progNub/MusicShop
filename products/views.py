from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from products.models import Product, Category, ProductImage, SubCategory
from django.db.models import F
from django.conf import settings
from django.http import Http404
from django.shortcuts import render


# Create your views here.


class Home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 50

    def get_queryset(self):
        products = Product.objects.annotate(first_image=F('images__image')).order_by('id')
        products = products.select_related('brand')
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'MEDIA_URL': settings.MEDIA_URL})
        return context


class HomeCategory(Home):

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category__slug=self.kwargs['category_slug'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        try:
            selected_sub_category = SubCategory.objects.get(slug=self.kwargs['category_slug'])
        except SubCategory.DoesNotExist:
            raise Http404('Выбранная подкатегория не существует')

        context.update({'selected_sub_category_slug': selected_sub_category.slug})
        return context


class HomeFeatures(Home):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(features=self.kwargs['category_id'])
        return queryset
