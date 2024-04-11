from django.db import models


class ProductSubFeature(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    sub_feature = models.ForeignKey('characteristic.SubFeature', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'feature_product'
        # unique_together = ('product', 'sub_feature')

    def __str__(self):
        return f"{self.product.name} - {self.sub_feature.name}: {self.value}"

    def __repr__(self):
        return f'{self.__class__.__name__} <{self.product.name}:{self.sub_feature.name}:{self.value}>'
