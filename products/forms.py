from django import forms

from characteristic.models import Feature
from common_models.models import ProductSubFeature
from .models import Product, CatalogItem, Brand, SubFeature
from django.forms import inlineformset_factory


class ProductSubFeatureForm(forms.ModelForm):
    class Meta:
        model = ProductSubFeature
        fields = ['sub_feature', 'value']
        widgets = {
            'sub_feature': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }


ProductSubFeatureFormSet = inlineformset_factory(
    Product, ProductSubFeature,
    form=ProductSubFeatureForm,
    extra=1,  # Количество пустых форм для начала
    can_delete=False,
)


class ProductForm(forms.ModelForm):
    inlines = [ProductSubFeatureFormSet]

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
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = CatalogItem.objects.all()
        self.fields['brand'].queryset = Brand.objects.all()
