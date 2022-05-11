from django import template

register = template.Library()


@register.simple_tag()
def multiply(a, b):
    return round(a * b)


@register.simple_tag()
def to_str(a):
    return str(a)
