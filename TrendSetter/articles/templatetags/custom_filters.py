from django.utils.html import mark_safe, strip_tags
from django import template

register = template.Library()

@register.filter
def sanitize(value):
    # Remove any unwanted HTML tags
    cleaned_value = strip_tags(value)
    return mark_safe(cleaned_value)