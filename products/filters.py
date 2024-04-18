# filters.py
from characteristic.models import Brand
from django_filters import widgets
from django.db.models import Count
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
        attrs = attrs or {}  # Убедитесь, что attrs не None
        attrs.update({'class': 'form-control mr-2'})  # Добавляем общий класс к виджету
        super().__init__(attrs)
        self.widgets[0].attrs.update({'placeholder': 'Цена от', })
        self.widgets[1].attrs.update({'placeholder': 'Цена до', })


class ProductFilter(django_filters.FilterSet):
    sort_by = django_filters.ChoiceFilter(
        choices=[
            ('price', 'По возрастанию'),
            ('-price', 'По убыванию'),
        ],
        method='sort_by_method',
        label='Сортировка:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Product
        fields = [
            'sort_by',
            'brand',
            'price',

        ]

    price = django_filters.RangeFilter(widget=CustomRangeWidget())

    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        field_name='brand',
        label='Производитель'
    )

    # Добавьте другие виджеты для других полей, если это необходимо

    def sort_by_method(self, queryset, name, value):
        print('Sort price method')
        print(self.data)

        if value is not None:
            if value == '-price':
                return queryset.order_by('-price')
            elif value == 'price':
                return queryset.order_by('price')

    def is_valid(self):
        is_valid = super().is_valid()
        print(self.data)

        return is_valid
