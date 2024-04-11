from django import forms
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

    def __init__(self, *args, **kwargs):
        super(ChooseDeliverymanForm, self).__init__(*args, **kwargs)
        self.fields['delivery'].queryset = Deliveryman.objects.all()
