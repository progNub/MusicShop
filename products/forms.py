from django import forms
from common_models.forms import ProductSubFeatureForm
from common_models.models import ProductSubFeature
from .models import Product, CatalogItem, Brand, ProductImage
from django.forms import inlineformset_factory


class CustomProductSubFeatureForm(ProductSubFeatureForm):

    def is_valid(self):
        product_sub_feature = self.cleaned_data.get('id')
        if self.cleaned_data.get('DELETE'):
            if product_sub_feature:
                ProductSubFeature.objects.get(id=product_sub_feature.id).delete()
        return super().is_valid()

    def save(self, commit=True):

        product_sub_feature = self.cleaned_data.get('id')
        sub_feature = self.cleaned_data.get('sub_feature')
        value = self.cleaned_data.get('value')
        product = self.cleaned_data.get('product')
        product_sub_feature_list = ProductSubFeature.objects.filter(sub_feature=sub_feature, product=product)

        if not product_sub_feature_list:
            return super().save(commit=True)
        for i in product_sub_feature_list:
            if not i.product == product and i.sub_feature == sub_feature and i.value == value:

                return super().save(commit=True)
            elif i.product == product and i.sub_feature == sub_feature and i.value != value:

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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductModelForm(forms.ModelForm):
    images = MultipleFileField(label='Select files', required=False)

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            for f in self.files.getlist('images'):
                ProductImage.objects.create(product=instance, image=f)
        return instance
