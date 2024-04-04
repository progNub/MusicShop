from django import template
from products.models import Feature, ProductSubFeature

register = template.Library()


@register.inclusion_tag(filename='inc/tag_list_feature.html')
def get_features(features: [str] = ''):
    list_feature = Feature.objects.all().prefetch_related('sub_feature')
    return {'list_feature': list_feature}

