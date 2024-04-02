from django import template
from products.models import Category

register = template.Library()


@register.inclusion_tag(filename='inc/products/tag_list_category.html')
def get_categories(selected_sub_category: dict):
    categories = Category.objects.prefetch_related('sub_category')

    selected_category = Category.objects.filter(sub_category__name=selected_sub_category).first()
    if selected_category:
        selected_category = selected_category.name

    context = {
        'categories': categories,
        'selected_sub_category': selected_sub_category,
        'selected_category': selected_category
    }

    return context
