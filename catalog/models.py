from django.db import models
from slugify import slugify
from mptt.models import MPTTModel, TreeForeignKey


def get_slug_catalog_item(model: 'CatalogItem'):
    names = []
    current = model
    while current.parent is not None:
        names.insert(0, current.parent.name)
        current = current.parent
    names.append(model.name)
    original_slug = '-'.join(names)
    return slugify(original_slug)


class CatalogItem(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug=get_slug_catalog_item(model=self)
        super(CatalogItem, self).save(*args, **kwargs)
