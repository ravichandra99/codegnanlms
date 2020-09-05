from django import template

register = template.Library()


@register.simple_tag
def show_type(data):
    f = open('jsondata.txt', 'w')
    f.write(data)

    return type(data)


@register.simple_tag
def get_dict_val(obj, key):
    return obj[1].get(key)


def to_string(value):
    return str(value)


register.filter('to_string', to_string)
