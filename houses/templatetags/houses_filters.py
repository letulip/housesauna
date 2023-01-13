from django import template

register = template.Library()


@register.filter(name='concat')
def concat(value, arg):
    """
    Concats integer index to given url stirng
    """

    return value + str(arg)
