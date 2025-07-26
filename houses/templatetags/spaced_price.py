from django import template

register = template.Library()


@register.filter
def spaced_price(value):
    """Кастомный обработчик отображения цены для клиента в шаблоне."""
    try:
        value = int(value)
        return '{:,}'.format(value).replace(',', ' ')
    except (ValueError, TypeError):
        return value
