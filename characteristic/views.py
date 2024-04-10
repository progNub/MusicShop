from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from characteristic.forms import SubFeatureForm, FeatureForm, BrandForm
from characteristic.models import Brand, Feature, SubFeature
from django.views.generic import TemplateView


class BaseCreateView(CreateView):
    success_url = reverse_lazy('list-characteristic')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "Создание"
        context['name_page'] = "Создание"
        return context

    def form_valid(self, form: BrandForm):
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class CreateBrandView(BaseCreateView):
    model = Brand
    template_name = 'brand/create_brand.html'
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Создание Брэнда"
        return context


class CreateFeatureView(BaseCreateView):
    model = Feature
    template_name = 'feature/create_feature.html'
    form_class = FeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Создание Характеристики"
        return context


class CreateSubFeatureView(BaseCreateView):
    model = SubFeature
    template_name = 'subFeature/create_sub_feature.html'
    form_class = SubFeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Создание подхарактеристики"
        return context


class ListCharacteristicsView(TemplateView):
    template_name = 'characteristic/list_characteristic.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = Feature.objects.all()
        context['sub_features'] = SubFeature.objects.all()
        context['brands'] = Brand.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        brand_form = BrandForm()
        feature_form = FeatureForm()
        sub_feature_form = SubFeatureForm()
        context['brand_form'] = brand_form
        context['feature_form'] = feature_form
        context['sub_feature_form'] = sub_feature_form

        return self.render_to_response(context)
