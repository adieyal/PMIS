from django.http import HttpResponse
from django.template.response import TemplateResponse
from project.apps.api.reports.district_report import district_report_json

def district_dashboard(request):
    # get json from api app
    # add json to response context
    # add variables into html direct
    return TemplateResponse(request, 'reports2/district/index.html', district_report_json(2, 2013, 6))

def district_progress(request):
    return TemplateResponse(request, 'reports2/district/progress.html', {})

def district_perform(request):
    return TemplateResponse(request, 'reports2/district/perform.html', {})
