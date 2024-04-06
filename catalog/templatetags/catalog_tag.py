from django import template

from catalog.models import CatalogItem

register = template.Library()

from django.db.models import Prefetch


@register.inclusion_tag(filename='catalog/inc/catalog.html')
def show_catalog():
    # Предполагается, что у модели CatalogItem есть связь 'children' для дочерних элементов
    # Используем Prefetch для загрузки всех уровней дочерних элементов
    child_prefetch = Prefetch('children', queryset=CatalogItem.objects.all().prefetch_related(
        Prefetch('children', queryset=CatalogItem.objects.all())))

    category_tree = CatalogItem.objects.filter(level=0).prefetch_related(child_prefetch)
    context = {'category_tree': category_tree}
    return context
