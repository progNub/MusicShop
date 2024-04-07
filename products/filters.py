# filters.py
import django_filters
from django import forms

from characteristic.models import Brand
from .models import Product
from django_filters import widgets
import django_filters
from django import forms
from .models import Product


# 'lte' (less than or equal to) — "меньше или равно".
# 'gte' (greater than or equal to) — "больше или равно".
# 'in' — выборка объектов, у которых значение поля находится в указанном списке.
# 'startswith' и 'istartswith' — выборка объектов, у которых значение поля начинается с указанной подстроки (с учетом регистра для 'startswith' и без учета регистра для 'istartswith').
# 'endswith' и 'iendswith' — выборка объектов, у которых значение поля заканчивается на указанную подстроку (с учетом регистра для 'endswith' и без учета регистра для 'iendswith').
# 'contains' и 'icontains' — выборка объектов, у которых значение поля содержит указанную подстроку (с учетом регистра для 'contains' и без учета регистра для 'icontains').
# 'range' — выборка объектов, у которых значение поля находится в указанном диапазоне.


class CustomRangeWidget(widgets.RangeWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        # Установка разных плейсхолдеров для каждого поля
        self.widgets[0].attrs.update({'placeholder': 'От', 'class': 'form-control'})
        self.widgets[1].attrs.update({'placeholder': 'До', 'class': 'form-control'})


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['lt', 'gt'],
            'brand': ['exact'],
            # Добавьте другие поля, по которым хотите фильтровать
        }

    price = django_filters.RangeFilter(
        widget=CustomRangeWidget())

    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        field_name='brand',
        label='Производитель'
    )

    # Добавьте другие виджеты для других полей, если это необходимо
