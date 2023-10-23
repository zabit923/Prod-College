from django import template
import re

register = template.Library()

@register.filter()
def is_link(value):
    return bool(re.match(r'http(s)?://', value))
