from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from catalog.models import CatalogItem


@receiver(post_save, sender=CatalogItem)
def delete_cache_after_save_catalog_item(sender, instance: CatalogItem, **kwargs):
    instance.update_slugs()
    CatalogItem.delete_cache()


@receiver(post_delete, sender=CatalogItem)
def delete_cache_after_delete_catalog_item(sender, instance: CatalogItem, **kwargs):
    CatalogItem.delete_cache()
