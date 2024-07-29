from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def create_link(obj, args):
    url_name, id_attr_name, display_attr_name = args.split(',')
    url = reverse(url_name, args=[getattr(obj, id_attr_name)])
    display_value = getattr(obj, display_attr_name, obj.pk)
    return f'<a href="{url}">{display_value}</a>'


@register.filter
def join_by_comma(elements):
    return ', '.join(elements)


@register.filter
def map(value, arg):
    func, args = arg.split(':', 1)
    return [globals()[func](v, args) for v in value]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
