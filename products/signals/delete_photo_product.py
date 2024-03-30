from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from django.conf import settings

from products.models import ProductImage


@receiver(pre_delete, sender=ProductImage)
def delete_image_after_delete_product_image(sender, instance: ProductImage, **kwargs):
    file_path = settings.MEDIA_ROOT
    if file_path.exists():
        file_path_for_delete = file_path / instance.image.path
        if file_path_for_delete.exists():
            file_path_for_delete.unlink(missing_ok=False)
