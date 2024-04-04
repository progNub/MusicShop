from django import template
from products.models import Category
from django.http import Http404

register = template.Library()


@register.inclusion_tag(filename='inc/tag_list_category.html')
def get_categories(selected_sub_category_slug: str = ''):
    categories = Category.objects.prefetch_related('sub_category')
    context = {'categories': categories, 'selected_sub_category_slug': selected_sub_category_slug}

    if not selected_sub_category_slug:
        return context

    try:
        selected_category = Category.objects.get(sub_category__slug=selected_sub_category_slug)
        context['selected_category_slug'] = selected_category.slug
    except Category.DoesNotExist:
        raise Http404('Выбранная категория не существует')

    return context
