from django import forms
from django.core.exceptions import ValidationError
from common_models.models import ProductSubFeature


class ProductSubFeatureForm(forms.ModelForm):

    class Meta:
        model = ProductSubFeature
        fields = ['sub_feature', 'value']
        widgets = {
            'sub_feature': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }

