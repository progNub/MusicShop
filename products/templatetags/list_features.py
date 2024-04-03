from django import template
from products.models import Feature, ProductFeature

register = template.Library()


@register.inclusion_tag(filename='inc/products/tag_list_feature.html')
def get_features(features: [str] = ''):
    context: dict = {}
    list_feature = Feature.objects.all()
    context.update({'list_feature': list_feature})
    return context
