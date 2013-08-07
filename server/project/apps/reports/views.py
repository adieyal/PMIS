from django.http import HttpResponse
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import json
from django.template.response import TemplateResponse
from project.apps.api.reports.district_report import district_report_json
from project.apps.projects import models
from django.views.decorators.cache import cache_page

@cache_page(60 * 10)
def district_dashboard(request, district_id, year, month):
    date = datetime(int(year), int(month), 1)
    return TemplateResponse(request, 'reports/district/index.html', district_report_json(district_id, date))

@cache_page(60 * 10)
def district_progress(request, district_id, year, month):
    date = datetime(int(year), int(month), 1)
    return TemplateResponse(request, 'reports/district/progress.html', district_report_json(district_id, date))

@cache_page(60 * 10)
def district_perform(request, district_id, year, month):
    date = datetime(int(year), int(month), 1)
    return TemplateResponse(request, 'reports/district/perform.html', district_report_json(district_id, date))

