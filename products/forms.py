from django import forms

from common_models.forms import ProductSubFeatureForm
from common_models.models import ProductSubFeature
from .models import Product, CatalogItem, Brand, SubFeature
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError


class CustomProductSubFeatureForm(ProductSubFeatureForm):

    def is_valid(self):
        product_sub_feature = self.cleaned_data.get('id')
        if self.cleaned_data.get('DELETE'):
            if product_sub_feature:
                ProductSubFeature.objects.get(id=product_sub_feature.id).delete()
        return super().is_valid()

    def save(self, commit=True):
        print('Saving')
        product_sub_feature = self.cleaned_data.get('id')
        sub_feature = self.cleaned_data.get('sub_feature')
        value = self.cleaned_data.get('value')
        product = self.cleaned_data.get('product')
        product_sub_feature_list = ProductSubFeature.objects.filter(sub_feature=sub_feature, product=product)
        print(product_sub_feature_list)
        if not product_sub_feature_list:
            print('Сохраняю новое')
            return super().save(commit=True)
        for i in product_sub_feature_list:
            if not i.product == product and i.sub_feature == sub_feature and i.value == value:
                print('новая запись')
                return super().save(commit=True)
            elif i.product == product and i.sub_feature == sub_feature and i.value != value:
                print('изменение записи')
                i.value = value
                i.save()
                return i
            elif i.id == product_sub_feature and (i.value != value or i.sub_feature != sub_feature):
                i.value = value
                i.sub_feature = sub_feature
                i.save()
                return i
            elif product_sub_feature == '' and sub_feature != i.sub_feature:
                return super().save(commit=True)


ProductSubFeatureFormSetCreate = inlineformset_factory(
    Product,
    ProductSubFeature,
    form=ProductSubFeatureForm,
    extra=1,  # Количество пустых форм для начала
    can_delete=False,
)

ProductSubFeatureFormSetUpdate = inlineformset_factory(
    Product,
    ProductSubFeature,
    form=CustomProductSubFeatureForm,
    extra=0,  # Количество пустых форм для начала
    can_delete=True,
)


class ProductModelForm(forms.ModelForm):
    inlines = []

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = CatalogItem.objects.all()
        self.fields['brand'].queryset = Brand.objects.all()
