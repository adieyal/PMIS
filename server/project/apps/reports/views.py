from django.http import HttpResponse
from django.template.response import TemplateResponse
from project.apps.api.reports.district_report import district_report_json, district_report_json2
from project.apps.projects import models

def district_dashboard(request, district_id, year, month):
    return TemplateResponse(request, 'reports/district/index.html', district_report_json(district_id, year, month))

def district_progress(request, district_id, year, month):
    return TemplateResponse(request, 'reports/district/progress.html', district_report_json(district_id, year, month))

def district_perform(request, district_id, year, month):
    return TemplateResponse(request, 'reports/district/perform.html', {})
