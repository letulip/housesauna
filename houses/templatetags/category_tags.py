from django import template
from houses.views import get_menu_categories

register = template.Library()


@register.inclusion_tag('includes/category_dropdown.html', takes_context=True)
def category_menu(context):
    """
    Тег для отображения выпадающего меню категорий.
    Меню всегда формируется из категорий верхнего уровня с флагами is_size, is_floor, is_selection.
    Использует единую функцию get_menu_categories для получения категорий.
    """
    saunas_list = context.get('saunas_list')
    houses_list = context.get('houses_list')
    if saunas_list is not None:
        related_name = 'saunas'
        is_saunas = True
        is_houses = False
    elif houses_list is not None:
        related_name = 'houses'
        is_saunas = False
        is_houses = True
    else:
        related_name = 'houses'
        is_saunas = False
        is_houses = True
    size_categories, floor_categories, selection_categories = get_menu_categories(related_name)

    return {
        'size_categories': size_categories,
        'floor_categories': floor_categories,
        'selection_categories': selection_categories,
        'saunas_list': is_saunas,
        'houses_list': is_houses,
        'curr_category': None,
    }
