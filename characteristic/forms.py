from django import forms
from characteristic.models import Feature
from common_models.models import ProductSubFeature
from products.models import Product
from .models import Brand, SubFeature
from django.forms import inlineformset_factory


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SubFeatureForm(forms.ModelForm):
    class Meta:
        model = SubFeature
        fields = ['name', 'feature']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'feature': forms.Select(attrs={'class': 'form-control'}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
