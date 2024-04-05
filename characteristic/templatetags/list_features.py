from django import template
from characteristic.models import Feature

register = template.Library()


@register.inclusion_tag(filename='characteristic/inc/tag_list_feature.html')
#TODO сделать получение характеристик
def get_features(features: [str] = ''):
    list_feature = Feature.objects.all().prefetch_related('sub_feature')
    return {'list_feature': list_feature}

