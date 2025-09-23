from django import template

register = template.Library()


@register.filter(name='concat')
def concat(value, arg):
    """
    Concats integer index to given url stirng
    """

    return value + str(arg)


@register.filter
def has_category(structure, name: str) -> bool:
    """
    True, если у объекта (House/Sauna) есть категория с именем, содержащим name (без учета регистра).
    Пример: structure|has_category:"Проект"
    """
    if not getattr(structure, "category", None):
        return False
    return structure.category.filter(name__icontains=name).exists()
