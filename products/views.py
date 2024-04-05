from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from common_models.models import ProductSubFeature
from products.models import Product, ProductImage
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


class DetailProduct(DetailView):
    model = Product
    template_name = 'products/page_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    pk_kwarg = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('brand')
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
