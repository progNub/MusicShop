from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy, reverse
from characteristic.forms import SubFeatureForm, FeatureForm, BrandForm
from characteristic.mixin import StaffOrSuperuserRequiredMixin
from characteristic.models import Brand, Feature, SubFeature
from django.views.generic import TemplateView


class BaseCreateView(StaffOrSuperuserRequiredMixin, CreateView):
    success_url = reverse_lazy('list-characteristic')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "Создание"
        context['name_page'] = "Создание"
        return context


class BaseUpdateView(StaffOrSuperuserRequiredMixin, UpdateView):
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('list-characteristic')


class BaseDeleteView(StaffOrSuperuserRequiredMixin, DeleteView):
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('list-characteristic')


class CreateBrandView(BaseCreateView):
    model = Brand
    template_name = 'brand/create_brand.html'
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Создание Брэнда"
        return context


class UpdateBrandView(BaseUpdateView):
    model = Brand
    template_name = 'brand/update_brand.html'
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Изменение производителя"
        return context


class DeleteBrandView(BaseDeleteView):
    model = Brand
    template_name = 'brand/delete_brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Удаление производителя"
        return context


class CreateFeatureView(BaseCreateView):
    model = Feature
    template_name = 'feature/create_feature.html'
    form_class = FeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Создание Характеристики"
        return context


class UpdateFeatureView(BaseUpdateView):
    model = Feature
    template_name = 'feature/update_feature.html'
    form_class = FeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Изменение производителя"
        return context


class DeleteFeatureView(BaseDeleteView):
    model = Feature
    template_name = 'feature/delete_feature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Удаление характеристики"
        return context


class CreateSubFeatureView(BaseCreateView):
    model = SubFeature
    template_name = 'subFeature/create_sub_feature.html'
    form_class = SubFeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Создание подхарактеристики"
        return context


class ListCharacteristicsView(StaffOrSuperuserRequiredMixin, TemplateView):
    template_name = 'characteristic/list_characteristic.html'

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


class UpdateSubFeatureView(BaseUpdateView):
    model = SubFeature
    template_name = 'subFeature/update_sub_feature.html'
    form_class = SubFeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Изменение подхарактеристики"
        return context


class DeleteSubFeatureView(BaseDeleteView):
    model = SubFeature
    template_name = 'subFeature/delete_sub_feature.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_page'] = "Удаление подхарактеристики"
        return context
