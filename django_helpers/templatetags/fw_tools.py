from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def get_element(object_, attribute_name):
    if object_ is None:
        return None
    return getattr(object_, attribute_name)


@register.filter
def getter(obj, key):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(key, None)
    else:
        if hasattr(obj, key):
            return getattr(obj, key)
    return None
