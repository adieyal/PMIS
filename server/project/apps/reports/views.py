from django.http import HttpResponse
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import json
from django.template.response import TemplateResponse
from project.apps.api.reports.district_report import district_report_json
from project.apps.projects import models
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect
from django.conf import settings

def test(request):
    date = datetime(2013, 6, 1)
    district_report_json(2, date)
    return TemplateResponse(request, 'test.html', {})

@cache_page(settings.API_CACHE)
def district_dashboard(request, district_id, year, month):
    date = datetime(int(year), int(month), 1)
    return TemplateResponse(request, 'reports/district/index.html', district_report_json(district_id, date))

@cache_page(settings.API_CACHE)
def district_progress(request, district_id, year, month):
    date = datetime(int(year), int(month), 1)
    return TemplateResponse(request, 'reports/district/progress.html', district_report_json(district_id, date))

@cache_page(settings.API_CACHE)
def district_perform(request, district_id, year, month):
    date = datetime(int(year), int(month), 1)
    return TemplateResponse(request, 'reports/district/perform.html', district_report_json(district_id, date))

@cache_page(settings.API_CACHE)
def generic_report(request, report, report_id, subreport, year, month):
    date = datetime(int(year), int(month), 1)
    template = 'reports/{report}/{subreport}.html'.format(report=report, subreport=subreport)
    context = {'json': None}
    return TemplateResponse(request, template, context)

@cache_page(settings.API_CACHE)
def generic_json(request, report, report_id, subreport, year, month):
    if report_id == None:
        return redirect('/api/reports/{report}/{subreport}/{year}/{month}/'.format(
                  report=report, subreport=subreport, year=year, month=month
                ))
    return redirect('/api/reports/{report}/{subreport}/{report_id}/{year}/{month}/'.format(
              report=report, subreport=subreport, report_id=report_id, year=year, month=month
            ))

