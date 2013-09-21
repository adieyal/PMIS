import format
from django import template

register = template.Library()

@register.filter(name="format_number")
def format_number(value):
    return format.format_number(value)

@register.filter(name="format_currency")
def format_currency(value):
    return format.format_currency(value)

@register.filter(name="format_percentage")
def format_percentage(value):
    return format.format_percentage(value)
