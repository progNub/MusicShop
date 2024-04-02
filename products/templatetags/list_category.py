from django import template
from products.models import Category
from django.http import Http404

register = template.Library()


@register.inclusion_tag(filename='inc/products/tag_list_category.html')
def get_categories(selected_sub_category_slug: dict):
    categories = Category.objects.prefetch_related('sub_category')

    try:
        selected_category = Category.objects.filter(sub_category__slug=selected_sub_category_slug).first()
    except Category.DoesNotExist:
        raise Http404('Выбранная подкатегория не существует')

    context: dict = {}
    if selected_category:
        context = {'selected_category_slug': selected_category.slug}

    context.update(
        {
            'categories': categories,
            'selected_sub_category_slug': selected_sub_category_slug,
        }
    )

    return context
