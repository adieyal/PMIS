import os
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
import fuzzywuzzy.process

from widgets import *
from database import Project
import iso8601

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

with open(os.path.join(settings.DJANGO_ROOT, 'locations.json')) as f:
    location_data = json.load(f)

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
def cluster_report(request, subreport, client_code, year, month):
    date = datetime(int(year), int(month), 1)
    template = 'reports/{report}/{subreport}.html'.format(report="cluster", subreport=subreport)
    context = {'json': None}
    return TemplateResponse(request, template, context)

#@cache_page(settings.API_CACHE)
def generic_report(request, report, report_id, subreport, year, month):
    date = datetime(int(year), int(month), 1)
    template = 'reports/{report}/{subreport}.html'.format(report=report, subreport=subreport)
    context = {'json': None}
    return TemplateResponse(request, template, context)

@cache_page(settings.API_CACHE)
def generic_json(request, report, subreport, year, month, report_id=None, client_code=None):
    if report_id == None:
        if client_code != None:
            return redirect('/api/reports/{report}/{subreport}/{client_code}/{year}/{month}/'.format(
                     report=report, subreport=subreport, year=year, month=month,
                     client_code=client_code
                   ))        
        return redirect('/api/reports/{report}/{subreport}/{year}/{month}/'.format(
                  report=report, subreport=subreport, year=year, month=month
                ))
    return redirect('/api/reports/{report}/{subreport}/{report_id}/{year}/{month}/'.format(
              report=report, subreport=subreport, report_id=report_id, year=year, month=month
            ))


def project_list(request):
    projects = Project.list()
    context = {
        'projects': projects,
        'year': '2013',
        'month': '12'
    }
    return TemplateResponse(request, 'reports/projects.html', context)
    

#@cache_page(settings.API_CACHE)
def project_json(request, project_id, year, month):
    
    def _date(date):
        try:
            dt = iso8601.parse_date(date)
        except iso8601.ParseError:
            return ''
        return dt.strftime('%d %B %Y')
    
    def _months(date1, date2):
        try:
            dt1 = iso8601.parse_date(date1)
            dt2 = iso8601.parse_date(date2)
        except iso8601.ParseError:
            return ''
        td = dt1 - dt2
        sec = td.total_seconds()
        months = (sec*12) / (86400*365)
        return '%.1f months' % (months)
        
    def _currency(value):
        try:
            value = int(value)
        except ValueError:
            return ''
        return 'R{:,.0f}'.format(value)
        
    def _percent(value):
        try:
            value = float(value)
        except ValueError:
            return ''
        return '%.0f%%' % (value*100)
        
    def _expenditure_for_month(data, month):
        for item in data:
            if iso8601.parse_date(item['date']).month == month:
                return item['expenditure']
        return ''

    def _progress_for_month(data, month):
        for item in data:
            if iso8601.parse_date(item['date']).month == month:
                try:
                    return float(item['progress'])/100
                except ValueError:
                    return ''
        return ''
        
    
    items = Project.list()
    project = Project.get(project_id)
    
    map_url = None
    result = fuzzywuzzy.process.extractOne(project.location, location_data['mainplaces'])
    if result:
        mp, score = result
        if score > 70:
            map_url = 'MP_CODE/%d.png' % (location_data['mainplace_codes'][mp])
    
    if map_url == None:
        result = fuzzywuzzy.process.extractOne(project.municipality, location_data['municipalities'])
        if result:
            mn, score = result
            if score > 70:
                map_url = 'MN_CODE/%d.png' % (location_data['municipality_codes'][mn])
    
    if map_url == None:
        map_url = 'fallback.png'
        
    map_url = 'http://s3.amazonaws.com/tasks.acscomputers.co.za/out/' + map_url
    
    context = {
        'agent': project.implementing_agent,
        'budget-donut': build_donut([0.15, 0.85], percentage=True),
        'budget-financial-year': _currency(project.allocated_budget_for_year),
        'budget-implementation': 'MISSING',
        'budget-increase-timeframe': _months(project.actual_completion, project.planned_completion),
        'budget-overall': _currency(project.total_anticipated_cost),
        'budget-planning': 'MISSING',
        'budget-slider': build_slider(project.expenditure_to_date, project.total_anticipated_cost),
        'budget-source': project.source,
        'budget-variation-orders': 'None', #TODO: This value is still missing from the IDIP.
        'cluster': 'MISSING',
        'comments-current': project.comments,
        'comments-previous': '',
        'comments-status': 'MISSING',
        'completion-date-actual': _date(project.actual_completion),
        'completion-date-planned': _date(project.planned_completion),
        'completion-date-revised': _date(project.revised_completion),
        'consultant': project.principal_agent,
        'contractor': project.contractor,
        'coordinator': project.manager,
        'district': project.district,
        'duration': _months(project.actual_completion, project.actual_start),
        'end_year': 'MISSING',
        'expenditure-actual': _currency(project.expenditure_to_date),
        'expenditure-cashflow-line': {
            'title': 'Expenditure vs Cashflow',
            'data': [
                {'values': [[i, d['expenditure']/1000] for i, d in enumerate(project.actual)], 'label': 'Cashflow'},
                {'values': [[i, d['expenditure']/1000] for i, d in enumerate(project.planning)], 'label': 'Expenditure'}
            ]
        },
        'expenditure-implementation-bar': {
            'title': 'Expenditure on implementation vs Budget on implementation',
            'data': [
                {'value': 2313, 'label': 'Expenditure on implementation'},
                {'value': 7365, 'label': 'Budget for implementation'}
            ]
        },
        'expenditure-percent': _percent(project.expenditure_percent_of_budget),
        'expenditure-planning-bar': {
            'title': 'Expediture on planning vs Budget for planning',
            'data': [
                {'value': 2313, 'label': 'Expenditure on planning'},
                {'value': 7365, 'label': 'Budget for planning'}
            ]
        },
        'expenditure-previous': _currency(project.total_previous_expenses),
        'expenditure-this-month': _currency(_expenditure_for_month(project.actual, int(month))),
        'expenditure-this-year': _currency(project.expenditure_in_year),
        'extensions': 'None', #TODO: This value is still missing from the IDIP.
        'implementation-handover-date': _date(project.implementation_handover),
        'jobs': 'MISSING',
        'location': '%s, %s' % (project.location, project.municipality) if project.location else project.municipality,
        'location_map': map_url,
        'mitigations-current': project.remedial_action,
        'mitigations-previous': '',
        'month': MONTHS[int(month)-1],
        'name': project.description,
        'number': project.contract,
        'phase': project.phase,
        'planning-completion-date-actual': _date(project.planning_completion),
        'planning-start-date-actual': _date(project.planning_start),
        'progress-gauge': build_gauge(_progress_for_month(project.planning, int(month))*100, _progress_for_month(project.actual, int(month))*100),
        'progress-slider': build_slider(project.expenditure_to_date, project.total_anticipated_cost),
        'progress-to-date': _percent(_progress_for_month(project.actual, int(month))),
        'scope': project.scope,
        'stage': [project.phase, _progress_for_month(project.actual, int(month))*100 if project.phase == 'implementation' else None],
        'start-date-actual': _date(project.actual_start),
        'start-date-planned': _date(project.planned_start),
        'year': '%d/%d' % (int(project.fyear)-1, int(project.fyear))
    }
    return HttpResponse(json.dumps(context), mimetype='application/json')
