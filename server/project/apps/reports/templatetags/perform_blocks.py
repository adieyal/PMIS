from django import template
from django.template.defaultfilters import stringfilter
from django.template import Template, Context
from format import format_currency, format_percentage

register = template.Library()

@register.simple_tag(takes_context=False)
def overunder_expenditure(actual, planned):
    difference = abs(actual - planned)
    if actual > planned:
        return "Over expenditure: %s" % format_currency(difference)
    elif actual < planned:
        return "Under expenditure: %s" % format_currency(difference)
    else:
        return "On budget"

@register.simple_tag(takes_context=False)
def overunder_percentage(actual, planned):
    difference = abs(actual - planned)
    if planned == 0:
        return "No expenditure planned"
    if actual > planned:
        return "%s over budget" % format_percentage(difference / planned * 100)
    elif actual < planned:
        return "%s under budget" % format_percentage((1 - difference / planned) * 100)
    else:
        return ""

