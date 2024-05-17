from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from common_models.models import ProductSubFeature
from products.filters import ProductFilter
from products.forms import ProductModelForm, ProductSubFeatureFormSetUpdate, ProductSubFeatureFormSetCreate
from products.mixins import StaffOrSuperuserRequiredMixin
from products.models import Product
from django.db.models import Q

from django.urls import reverse_lazy
from django.db import transaction

from urllib.parse import urlencode

# Create your views here.

class Home(FilterView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 20
    filterset_class = ProductFilter

    from urllib.parse import urlencode

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_product = self.request.GET.get('search_product')

        # Создаём копию объекта запроса, чтобы можно было изменять параметры
        get_copy = self.request.GET.copy()
        if 'page' in get_copy:
            del get_copy['page']  # Удаляем параметр 'page', чтобы избежать конфликтов

        # Создаём строку запроса для использования в шаблоне
        context['get_params'] = urlencode(get_copy)
        context.update({'search_product': search_product})
        return context

    def get_queryset(self):
        products = Product.objects.filter(availability=True).order_by('name')
        products = products.select_related('brand')
        products = products.prefetch_related('images')

        query_search = self.request.GET.get('search_product')
        if query_search:
            products = products.filter(Q(name__icontains=query_search) | Q(
                description__icontains=query_search))
        return products


class DetailProduct(DetailView):
    model = Product
    template_name = 'products/page_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
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


class CreateProduct(StaffOrSuperuserRequiredMixin, CreateView):
    model = Product
    template_name = 'products/create_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    form_class = ProductModelForm

    def __init__(self):
        super().__init__()
        self.form_class.inlines.append(ProductSubFeatureFormSetCreate)

    def get_context_data(self, **kwargs):
        context = super(CreateProduct, self).get_context_data(**kwargs)
        if 'formset' not in context:
            formset = ProductSubFeatureFormSetCreate(self.request.POST or None)
            context['formset'] = formset
        return context

    @transaction.atomic
    def form_valid(self, form: ProductModelForm):
        context = self.get_context_data()
        formset = context['formset']
        product = form.save(commit=False)

        if formset.is_valid():
            product.save()
            formset.instance = product
            formset.save()
            return super(CreateProduct, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        product = self.object
        return reverse_lazy('show-product', args=[product.slug])


class UpdateProduct(StaffOrSuperuserRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/update_product.html'
    context_object_name = 'product'
    form_class = ProductModelForm
    slug_url_kwarg = 'slug'

    def __init__(self):
        super().__init__()
        self.form_class.inlines.append(ProductSubFeatureFormSetUpdate)

    def get_context_data(self, **kwargs):
        context = super(UpdateProduct, self).get_context_data(**kwargs)
        if 'formset' not in context:
            formset = self.form_class.inlines[0](self.request.POST or None, instance=self.object)
            context['formset'] = formset
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        formset: ProductSubFeatureFormSetUpdate = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super(UpdateProduct, self).form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('show-product', args=[self.object.slug])


class DeleteProduct(StaffOrSuperuserRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('home')
