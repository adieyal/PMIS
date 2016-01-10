import os
from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def app_settings():
    return os.getenv('DJANGO_SETTINGS_MODULE').replace('server.settings.', '')

@register.simple_tag
def app_redis_db():
    redis = settings.REDIS
    return redis['db']

@register.simple_tag
def app_sqlite_db():
    name = os.path.basename(settings.DATABASES['default']['NAME'])
    return name

@register.simple_tag
def fin_year(body, fin_year, attribute):
    return body['calculated']['financial_years'][fin_year][attribute]
