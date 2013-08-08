import locale
from django import template

register = template.Library()

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def _format_currency(value):
    if value == int(value):
        return "R" + locale.format("%d", value, grouping=True)
    else:
        return "R" + locale.format("%.2f", value, grouping=True)

def format_currency(value):
    return _format_currency(value)

register.filter('format_currency', format_currency)
