import locale
from django import template

register = template.Library()

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def _format_currency(value):
    try:
        if int(value) == 0:
            return "R0.00"
        elif value == int(value):
            return "R" + locale.format("%d", value, grouping=True)
        else:
            return "R" + locale.format("%.2f", value, grouping=True)
    except ValueError:
        return "-"

def _format_percentage(value):
    if int(value) == value:
        return "%d%%" % value
    else:
        return "%.1f%%" % value

def format_currency(value):
    return _format_currency(value)

def format_percentage(value):
    return _format_percentage(value)

register.filter('format_currency', format_currency)
register.filter('format_percentage', format_percentage)
