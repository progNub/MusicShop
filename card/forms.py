from django import forms

from accounts.models import AddressUser
from .models import Deliveryman, Order


class DeliverymanForm(forms.ModelForm):
    class Meta:
        model = Deliveryman
        fields = ['first_name', 'last_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChooseDeliverymanForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery']
        widgets = {
            'delivery': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        delivery = self.cleaned_data.get('delivery')
        if delivery is None:
            raise forms.ValidationError('Выберите курьера')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(ChooseDeliverymanForm, self).__init__(*args, **kwargs)
        self.fields['delivery'].queryset = Deliveryman.objects.all()



class AddressSelectionForm(forms.ModelForm):
    address = forms.ModelChoiceField(queryset=AddressUser.objects.none(), required=True, label='Адрес доставки')

    class Meta:
        model = AddressUser
        fields = ['address']
        widgets = {
            'address': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddressSelectionForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['address'].queryset = AddressUser.objects.filter(user=user)
