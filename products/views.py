from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from products.models import Product, Category, ProductImage, SubCategory, ProductSubFeature, Feature
from django.db.models import F
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.db.models import OuterRef, Subquery


# Create your views here.


class Home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 50

    def get_queryset(self):
        products = Product.objects.filter(availability=True).order_by('id')
        products = products.select_related('brand')
        image = ProductImage.objects.filter(
            product=OuterRef('pk')
        ).order_by('id')[:1]
        products = products.annotate(image=Subquery(image.values('image')[:1]))
        return products


class HomeCategory(Home):

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sub_category__slug=self.kwargs['sub_category_slug'])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)

        try:
            selected_sub_category = SubCategory.objects.get(slug=self.kwargs['sub_category_slug'])
        except SubCategory.DoesNotExist:
            raise Http404('Выбранная подкатегория не существует')

        context.update({'selected_sub_category_slug': selected_sub_category.slug})
        return context


class DetailProduct(DetailView):
    model = Product
    template_name = 'products/page_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    pk_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('brand', 'sub_category')
        queryset = queryset.prefetch_related('images')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product_sub_features = ProductSubFeature.objects.filter(product=product).select_related('sub_feature__feature')

        features: dict = {}
        for psf in product_sub_features:
            feature = psf.sub_feature.feature
            if feature not in features:
                features[feature] = []
            features[feature].append({'sub_feature': psf.sub_feature, 'value': psf.value})

        context.update({'features': features})
        return context
