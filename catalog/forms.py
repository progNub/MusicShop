from django import forms
from django.forms import models

import re
from django.db.models import Q
from django.core.exceptions import ValidationError
from catalog.models import CatalogItem, get_slug_catalog_item
from pprint import pprint

import time


def calculate_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result

    return wrapper


class CatalogItemForm(models.ModelForm):
    class Meta:
        model = CatalogItem
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.data.get('name')
        print('name')
        if CatalogItem.objects.filter(Q(name=name) & Q(parent__isnull=True)).exists():
            print('name already exists')
            raise ValidationError('Name already exists')
        else:
            cleaned_name = name
        return cleaned_name


class UpdateCatalogItemForm(forms.Form):
    class Meta:
        model = CatalogItem


    def clean_delete_fields(self):
        print('clean_new_fields')
        pattern = re.compile(r'#delete#')
        new_items = {}
        for key, value in self.data.items():
            if pattern.search(key):
                # Заменяем подстроку на пустую строку
                new_key = pattern.sub('', key)
                if new_key not in new_items.keys() and value != '':
                    new_items[new_key] = {value}
                else:
                    new_items[new_key].add(value)
        # pprint(new_items)
        return new_items

    def save_fields_to_delete(self):
        print("delete new items")
        objs = self.Meta.model.objects.filter(slug__in=self.clean_delete_fields().keys())
        for obj in objs:
            obj.delete()

    def clean_new_fields(self) -> dict[str, {str}]:
        print('clean_new_fields')
        pattern = re.compile(r'#new#\d+#')
        new_items = {}
        for key, value in self.data.items():
            if pattern.search(key):
                # Заменяем подстроку на пустую строку
                new_key = pattern.sub('', key)
                if new_key not in new_items.keys() and value != '':
                    new_items[new_key] = {value}
                else:
                    new_items[new_key].add(value)
        return new_items

    def save_new_items(self):
        print("saving new items")
        new_items = self.clean_new_fields()
        objs_parent = self.Meta.model.objects.filter(slug__in=new_items.keys())
        for obj_parent in objs_parent:
            for child_value in new_items.get(obj_parent.slug):
                if child_value not in [i.name for i in obj_parent.get_children()]:
                    CatalogItem(parent_id=obj_parent.id, name=child_value).save()

    @calculate_execution_time
    def clean(self):
        self.cleaned_data = []
        # pprint(dict(self.data))

        data = dict(self.data.items())
        data.pop('csrfmiddlewaretoken', None)

        # Проверка переданных данных на пустоту
        for slug_key, name_value in data.items():
            if name_value == '':
                self.errors[slug_key] = 'Поле "name" не может быть пустым'

        # Получение объектов на основе данных из запроса и создание словаря с этими объектами
        objs = self.Meta.model.objects.filter(slug__in=data.keys())
        items_dict = {}
        for obj in objs:
            items_dict[obj.slug] = obj

        for slug_key, name_value in data.items():
            # Проверка что, имя изменилось иначе не добавляем в cleaned
            if slug_key in items_dict.keys():
                if items_dict[slug_key].name != name_value:
                    items_dict[slug_key].name = name_value

                    # Создаем новый slug на основе нового имени
                    new_slug = get_slug_catalog_item(items_dict[slug_key])

                    #   Проверка на то что, такого slug еще нет в items_dict
                    if new_slug not in items_dict.keys():
                        items_dict[slug_key].slug = new_slug
                        self.cleaned_data.append(items_dict[slug_key])
                    else:
                        self.errors[slug_key] = f'Имя внутри подкаталога должно быть уникально'
        #
        # print('self.errors')
        # pprint(dict(self.errors))
        # print('self.cleaned_data ')
        # pprint(dict(self.cleaned_data))

        return self.cleaned_data

    @calculate_execution_time
    def save(self):
        print("Saving")

        # Обновляем объекты в bulk_update
        self.Meta.model.objects.bulk_update(self.cleaned_data, ['slug', 'name', ])
        self.Meta.model.delete_cache()
        # удаляем кэш каталога

        self.Meta.model.update_slugs()
        self.save_new_items()
        self.save_fields_to_delete()
