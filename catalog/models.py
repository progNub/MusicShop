from django.db import models
from slugify import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Prefetch
from django.core.cache import cache


def get_slug_catalog_item(model: 'CatalogItem'):
    names = []
    current = model
    while current.parent is not None:
        names.insert(0, current.parent.name)
        current = current.parent
    names.append(model.name)
    original_slug = '-'.join(names)
    slug = slugify(original_slug)
    return slug


class CatalogItem(MPTTModel):
    name = models.CharField(max_length=255, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True)

    class MPTTMeta:
        order_insertion_by = ['-level', 'id']

    @staticmethod
    def get_tree_items():
        cache_key = 'catalog_items_tree'
        cached_items = cache.get(cache_key)
        if cached_items is not None:
            return cached_items

        child_prefetch = Prefetch('children', queryset=CatalogItem.objects.all().prefetch_related(
            Prefetch('children', queryset=CatalogItem.objects.all())))
        queryset = CatalogItem.objects.filter(level=0).prefetch_related(child_prefetch)
        # Преобразование QuerySet в список перед кешированием
        items_list = list(queryset)
        # Кеширование на 1 час (или другое удобное вам время)
        cache.set(cache_key, items_list, timeout=3600)
        return items_list

    @classmethod
    def update_slugs(cls):
        """Обновляем значение slug для всех полей"""

        item_for_change = []
        all_items = cls.get_tree_items()
        for i in all_items:
            temp_slug = get_slug_catalog_item(i)
            if i.slug != temp_slug:
                i.slug = temp_slug
                item_for_change.append(i)

        if item_for_change:
            cls.objects.bulk_update(item_for_change, ['slug', ])

    @staticmethod
    def delete_cache():
        cache.delete('catalog_items_tree')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}<{self.slug}>'

    def save(self, *args, **kwargs):
        self.slug = get_slug_catalog_item(model=self)
        super(CatalogItem, self).save(*args, **kwargs)
