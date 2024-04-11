# templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='add_css_class')
def add_css_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})



from django.utils.html import mark_safe, strip_tags

register = template.Library()

@register.filter(name='sanitize')
def sanitize(value):
    cleaned_value = strip_tags(value)
    return mark_safe(cleaned_value)