import os
from django.http import HttpResponse
from datetime import datetime
from decimal import Decimal
from collections import OrderedDict
import json
from django.template.response import TemplateResponse
#from project.apps.api.reports.district_report import district_report_json
#from project.apps.projects import models
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings
import fuzzywuzzy.process

from widgets import *
from project.libs.database.database import Project
import iso8601
import calendar

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

with open(os.path.join(settings.DJANGO_ROOT, 'locations.json')) as f:
    location_data = json.load(f)

def test(request):
    date = datetime(2013, 6, 1)
    district_report_json(2, date)
    return TemplateResponse(request, 'test.html', {})

### Utility functions


def _safe_float(val):
    try:
        return float(filter(lambda x: x.isdigit() or x == '.', str(val)))
    except (TypeError, ValueError):
        return None
            
def _safe_int(val, add=0):
    try:
        return int(filter(lambda x: x.isdigit() or x == '.', str(val))) + add
    except (TypeError, ValueError):
        return None
                
def _date(date):
    try:
        dt = iso8601.parse_date(date)
    except iso8601.ParseError:
        return ''
    return dt.strftime('%d %B %Y')
    
def _months(date1, date2, alt_text=''):
    try:
        dt1 = iso8601.parse_date(date1)
        dt2 = iso8601.parse_date(date2)
    except iso8601.ParseError:
        return alt_text
    td = dt1 - dt2
    sec = td.total_seconds()
    months = (sec*12) / (86400*365)
    return '%.0f months' % (months)
        
def _currency(value):
    value = _safe_float(value)
    if value:
        return 'R{:,.0f}'.format(value)
    return ''
    
def _percent(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return ''
    return '%.0f%%' % (value*100)
        
def _expenditure_for_month(data, month):
    try:
        return data[month]['expenditure']
    except:
        return ''

def _progress_for_month(data, month):
    clean_data = [{
        'month': m,
        'progress': _safe_float(i['progress'])
    } for m, i in enumerate(data)]

    latest = None
    for item in clean_data:
        if item['month']<=month and item['progress'] != None:
            if not latest or latest['month'] < item['month']:
                latest = item
    if latest:
        return latest['progress']/100
        
    return 0
    
def _project_status(actual, planned):
    if (planned - actual) > 0.2:
        return ('In danger', 'red')
    elif (planned - actual) > 0.1:
        return ('Monitor Project', 'yellow')
    else:
        return ('On Target', 'green')

def _avg(values):
    if len(values) == 0:
        return ''
    return sum(values)/float(len(values))

def _in_month(date, year, month):
    year = _safe_int(year)
    month = _safe_int(month)
    try:
        date = iso8601.parse_date(date).replace(tzinfo=None)
    except iso8601.ParseError:
        return False
    if date < datetime(year, month, 1, 0, 0, 0, 0):
        return False
    due_month = (month % 12) + 1
    due_year = year + (month // 12)
    due_day = calendar.monthrange(due_year, due_month)[1]
    due = datetime(due_year, due_month, due_day, 23, 59, 59, 0)
    return date < due

def _in_3months(date, year, month):
    year = _safe_int(year)
    month = _safe_int(month)
    try:
        date = iso8601.parse_date(date).replace(tzinfo=None)
    except iso8601.ParseError:
        return False
    if date < datetime(year, month, 1, 0, 0, 0, 0):
        return False
    due_month = ((month + 2) % 12) + 1
    due_year = year + ((month + 2) // 12)
    due_day = calendar.monthrange(due_year, due_month)[1]
    due = datetime(due_year, due_month, due_day, 23, 59, 59, 0)
    return date < due

def _in_financial_year(date, year, month):
    year = _safe_int(year)
    month = _safe_int(month)
    if month < 4:
        fyear = year
    else:
        fyear = year + 1
    try:
        date = iso8601.parse_date(date).replace(tzinfo=None)
    except iso8601.ParseError:
        return False
    if date < datetime(year, month, 1, 0, 0, 0, 0):
        return False
    due_month = 3 # March of the financial year.
    due_year = fyear
    due_day = calendar.monthrange(due_year, due_month)[1]
    due = datetime(due_year, due_month, due_day, 23, 59, 59, 0)
    return date < due

###


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

@cache_page(settings.API_CACHE)
def generic_report(request, report, report_id, subreport, year, month):
    date = datetime(int(year), int(month), 1)
    template = 'reports/{report}/{subreport}.html'.format(report=report, subreport=subreport)
    context = {'json': None}
    return TemplateResponse(request, template, context)

#@cache_page(settings.API_CACHE)
def project_report(request, project_id):
    template = 'reports/project/project.html'
    context = { 'json': None }
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
def project_json(request, project_id, year=None, month=None):
    if not year or not month:
        project = Project.get(project_id)
        year = project.timestamp.year
        month = '%02d' % (project.timestamp.month)
    else:
        year = int(year)
        month = month
        project = Project.get(project_id)
        
    # Convert month number to 0 indexed month.
    MONTHS0 = {
        '04': (0, 1),  '05': (1, 1),  '06': (2, 1),
        '07': (3, 1),  '08': (4, 1),  '09': (5, 1),
        '10': (6, 1),  '11': (7, 1),  '12': (8, 1),
        '01': (9, 0),  '02': (10, 0), '03': (11, 0)
    }
    month0, year_add = MONTHS0[month]
    year += year_add

    def _safe_float(val):
        try:
            return float(filter(lambda x: x.isdigit(), val))
        except (TypeError, ValueError):
            return None
            
    def _safe_int(val, add=0):
        try:
            return int(filter(lambda x: x.isdigit(), val)) + add
        except (TypeError, ValueError):
            return None
                
    def _date(date):
        try:
            dt = iso8601.parse_date(date)
        except iso8601.ParseError:
            return ''
        return dt.strftime('%d %B %Y')
    
    def _months(date1, date2, alt_text=''):
        try:
            dt1 = iso8601.parse_date(date1)
            dt2 = iso8601.parse_date(date2)
        except iso8601.ParseError:
            return alt_text
        td = dt1 - dt2
        sec = td.total_seconds()
        months = (sec*12) / (86400*365)
        return '%.0f months' % (months)
        
    def _currency(value):
        value = _safe_int(value)
        if value:
            return 'R{:,.0f}'.format(value)
        return ''
        
    def _percent(value):
        try:
            value = float(value)
        except (ValueError, TypeError):
            return ''
        return '%.0f%%' % (value*100)
        
    def _expenditure_for_month(data, month):
        try:
            return data[month]['expenditure']
        except:
            return ''

    def _progress_for_month(data, month):
        clean_data = [{
            'month': m,
            'progress': _safe_float(i['progress'])
        } for m, i in enumerate(data)]

        latest = None
        for item in clean_data:
            if item['month']<=month and item['progress'] != None:
                if not latest or latest['month'] < item['month']:
                    latest = item
        if latest:
            return latest['progress']/100
        
        return 0
    
    def _project_status(actual, planned):
        if (planned - actual) > 0.2:
            return ('In danger', 'red')
        elif (planned - actual) > 0.1:
            return ('Monitor Project', 'yellow')
        else:
            return ('On Target', 'green')
    
    items = Project.list()
    project = Project.get(project_id)
    
    map_url = None
    result = fuzzywuzzy.process.extractOne(project.municipality, location_data['municipalities'])
    if result:
        mn, score = result
        if score > 70:
            map_url = settings.STATIC_URL + 'img/municipalities/%s' % (location_data['municipality_files'][mn])

    if map_url == None:
        map_url = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='

    district_map_url = None
    result = fuzzywuzzy.process.extractOne(project.district, location_data['districts'])
    if result:
        district, score = result
        if score > 70:
            district_map_url = settings.STATIC_URL + 'img/districts/%s' % (location_data['district_files'][district])
    
    if district_map_url == None:
        district_map_url = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
        
    def _budget_donut(planning, implementation):
        planning = _safe_float(planning) or 0
        implementation = _safe_float(implementation) or 0
        total = planning+implementation
        if total == 0:
            return build_donut([], percentage=True)
        return build_donut([
            planning / total,
            implementation / total
        ], percentage=True)
            
    
    context = {
        'agent': project.implementing_agent,
        'budget-donut': _budget_donut(project.budget_planning, project.budget_implementation),
        'budget-financial-year': _currency(project.allocated_budget_for_year),
        'budget-implementation': _currency(project.budget_implementation),
        'budget-increase-timeframe': _months(project.actual_completion, project.planned_completion, 'No increase'),
        'budget-overall': _currency(project.total_anticipated_cost),
        'budget-planning': _currency(project.budget_planning),
        'budget-slider': build_slider(project.expenditure_to_date, project.total_anticipated_cost),
        'budget-source': project.source,
        'budget-variation-orders': _currency(project.budget_variation_orders),
        'cluster': project.cluster,
        'comments-current': project.comments,
        'comments-previous': project.comments_previous,
        'comments-stage': (project.phase or '').title(),
        'completion-date-actual': _date(project.actual_completion),
        'completion-date-planned': _date(project.planned_completion),
        'completion-date-revised': _date(project.revised_completion),
        'consultant': project.principal_agent,
        'contractor': project.contractor,
        'coordinator': project.manager,
        'district': project.district,
        'duration': _months(project.actual_completion, project.actual_start, None) or
                    _months(project.planned_completion, project.planned_start),
        'end_year': 'MISSING',
        'expenditure-actual': _currency(project.expenditure_to_date),
        'expenditure-cashflow-line': {
            'title': 'Expenditure vs Cashflow',
            'data': [
                {'values': [[i, (_safe_float(d['expenditure']) or 0)/1000] for i, d in enumerate(project.actual)], 'label': 'Cashflow'},
                {'values': [[i, (_safe_float(d['expenditure']) or 0)/1000] for i, d in enumerate(project.planning)], 'label': 'Expenditure'}
            ],
            'labels': ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                       'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar' ]
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
        'expenditure-this-month': _currency(_expenditure_for_month(project.actual, month0)),
        'expenditure-this-year': _currency(project.expenditure_in_year),
        'extensions': '%.0f months' % (_safe_float(project.extensions)) if _safe_float(project.extensions) else 'None',
        'implementation-handover-date': _date(project.implementation_handover),
        'jobs': _safe_int(project.jobs) or '',
        'location': '%s, %s' % (project.location, project.municipality) if project.location else project.municipality,
        'location_map': map_url,
        'district_map': district_map_url,
        'mitigations-current': project.remedial_action,
        'mitigations-previous': project.remedial_action_previous,
        'month': MONTHS[int(month)-1],
        'name': project.description,
        'number': project.contract,
        'phase': project.phase,
        'planning-completion-date-actual': _date(project.planning_completion),
        'planning-phase': project.planning_phase if project.phase == 'planning' else 'none',
        'planning-start-date-actual': _date(project.planning_start),
        'progress-gauge': build_gauge(_progress_for_month(project.planning, month0)*100, _progress_for_month(project.actual, month0)*100),
        'progress-slider': build_slider(project.expenditure_to_date, project.total_anticipated_cost),
        'progress-to-date': _percent(_progress_for_month(project.actual, month0)),
        'scope': project.scope,
        'stage': [project.phase, _progress_for_month(project.actual, month0)*100 if project.phase == 'implementation' else None],
        'status': _project_status(_progress_for_month(project.actual, month0),
                                  _progress_for_month(project.planning, month0))[0],
        'status-color': _project_status(_progress_for_month(project.actual, month0),
                                        _progress_for_month(project.planning, month0))[1],
        'start-date-actual': _date(project.actual_start),
        'start-date-planned': _date(project.planned_start),
        #'year': '%d/%d' % (_safe_int(project.fyear, -1), _safe_int(project.fyear)) if _safe_int(project.fyear) else 'Unknown'
        'year': '%d/%d' % (year-1, year) if year else 'Unknown'
    }
    return HttpResponse(json.dumps(context), mimetype='application/json')


#@cache_page(settings.API_CACHE)
def cluster_report(request, cluster, subreport=None):
    if not subreport:
        return redirect('cluster', cluster=cluster, subreport='dashboard')
    template = 'reports/cluster/{subreport}.html'.format(subreport=subreport)
    context = {
        'json': None,
        'districts': ['nkangala', 'gertsibande', 'ehlanzeni']
    }
    return TemplateResponse(request, template, context)

@cache_page(settings.API_CACHE)
def cluster_dashboard_json(request, cluster, year=None, month=None):
    projects = filter(
        lambda x: x.cluster.lower().replace(' ', '-') == cluster,
        [Project.get(p) for p in Project.list() if p]
    )
    programmes = set([p.programme for p in projects])
    programmes_implementation = set([p.programme for p in projects if p.phase == 'implementation'])

    if not year or not month:
        timestamp = max([project.timestamp for project in projects])
        year = timestamp.year
        month = '%02d' % (timestamp.month)
    else:
        year = int(year)
        month = month
        
    # Convert month number to 0 indexed month.
    MONTHS0 = {
        '04': (0, 1),  '05': (1, 1),  '06': (2, 1),
        '07': (3, 1),  '08': (4, 1),  '09': (5, 1),
        '10': (6, 1),  '11': (7, 1),  '12': (8, 1),
        '01': (9, 0),  '02': (10, 0), '03': (11, 0)
    }
    month0, year_add = MONTHS0[month]
    fyear = year + year_add
    
    context = {
        "client": projects[0].cluster,
        "year": '%d/%d' % (fyear-1, fyear) if fyear else 'Unknown',
        "month": MONTHS[int(month)-1],

        ### Summary section
        "total-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects])),
        "total-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects]),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects])
        ),
        "total-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects])),
        "total-progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation'])),
        "total-progress-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation'])
        ),
        "total-projects": len(projects),
        "total-projects-accounts": len([p for p in projects if p.phase == 'final-accounts']),
        "total-projects-implementation": len([p for p in projects if p.phase == 'implementation']),
        "total-projects-planning": len([p for p in projects if p.phase == 'planning']),
        ###
        ### Programmes section
        "programmes": [
            {
                "name": programme,
                "budget-slider": build_slider(
                    sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme]),
                    sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme])
                ),
                "projects-accounts": len([p for p in projects if p.programme == programme and p.phase == 'final-accounts']),
                "projects-implementation": len([p for p in projects if p.programme == programme and p.phase == 'implementation']),
                "projects-planning": len([p for p in projects if p.programme == programme and p.phase == 'planning']),
                "projects-total": len([p for p in projects if p.programme == programme]),
                "total-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme])) or 'R 0',
            } for programme in programmes if programme != '--------'
        ],
        ###
        ### Planning section
        "planning-projects-total": len([p for p in projects if p.phase == 'planning']),
        "planning-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'planning'])),
        "planning-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'planning'])),
        "planning-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'planning']),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'planning'])
        ),
        "planning-stage-appointment": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'consultant-appointment']),
        "planning-stage-design": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'design-consting']),
        "planning-stage-documentation": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'documentation']),
        "planning-stage-tendering": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'tender']),
        "planning-stage-donut": build_donut([
            len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'consultant-appointment']),
            len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'design-consting']),
            len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'documentation']),
            len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'tender']),
        ]),
        ###
        ### Implementation section
        "implementation-projects-total": len([p for p in projects if p.phase == 'implementation' or p.phase == 'completed']),
        "implementation-projects-completed": len([p for p in projects if p.phase == 'completed']),
        "implementation-projects-practical-completion": 0,
        "implementation-projects-final-completion": 0,
        "implementation-projects-due-3months": len([p for p in projects if p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
        "implementation-progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation'])),
        "implementation-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'implementation'])),
        "implementation-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'implementation'])),
        "implementation-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'implementation']),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'implementation'])
        ),
        "implementation-progress-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation'])
        ),
        
        ###
        ### Programmes in implementation section
        "programmes_implementation": [
            {
                "name": programme,
                "budget-slider": build_slider(
                    sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme]),
                    sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme])
                ),
                "projects-implementation": len([p for p in projects if p.programme == programme and p.phase == 'implementation']),
                "expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme])),
                "budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme])),
                "projects-0-50": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
                "projects-51-75": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
                "projects-76-99": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
                "projects-100": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
                "projects-donut": build_donut([
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
                ]),
            } for programme in programmes_implementation if programme != '--------'
        ],
        ###
        ### District summary section
        "district-nkangala-projects-implementation": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation']),
        "district-nkangala-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.district == 'Nkangala' and p.phase == 'implementation'])),
        "district-nkangala-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.district == 'Nkangala' and p.phase == 'implementation'])),
        "district-nkangala-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.district == 'Nkangala' and p.phase == 'implementation']),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.district == 'Nkangala' and p.phase == 'implementation'])
        ),
        "district-nkangala-projects-0-50": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
        "district-nkangala-projects-51-75": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
        "district-nkangala-projects-76-99": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
        "district-nkangala-projects-100": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
        "district-nkangala-projects-donut": build_donut([
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
        ]),
        
        "district-gertsibande-projects-implementation": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation']),
        "district-gertsibande-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation'])),
        "district-gertsibande-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation'])),
        "district-gertsibande-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation']),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation'])
        ),
        "district-gertsibande-projects-0-50": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
        "district-gertsibande-projects-51-75": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
        "district-gertsibande-projects-76-99": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
        "district-gertsibande-projects-100": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
        "district-gertsibande-projects-donut": build_donut([
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
        ]),
        
        "district-ehlanzeni-projects-implementation": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation']),
        "district-ehlanzeni-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation'])),
        "district-ehlanzeni-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation'])),
        "district-ehlanzeni-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation']),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation'])
        ),
        "district-ehlanzeni-projects-0-50": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
        "district-ehlanzeni-projects-51-75": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
        "district-ehlanzeni-projects-76-99": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
        "district-ehlanzeni-projects-100": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
        "district-ehlanzeni-projects-donut": build_donut([
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
        ]),
        ###
    }
    return HttpResponse(json.dumps(context), mimetype='application/json')

#@cache_page(settings.API_CACHE)
def cluster_progress_json(request, cluster, year=None, month=None):
    projects = filter(
        lambda x: x.cluster.lower().replace(' ', '-') == cluster,
        [Project.get(p) for p in Project.list() if p]
    )
    programmes = set([p.programme for p in projects])
    programmes_implementation = set([p.programme for p in projects if p.phase == 'implementation'])
    programmes_planning = set([p.programme for p in projects if p.phase == 'planning'])

    if not year or not month:
        timestamp = max([project.timestamp for project in projects])
        year = timestamp.year
        month = '%02d' % (timestamp.month)
    else:
        year = int(year)
        month = month
        
    # Convert month number to 0 indexed month.
    MONTHS0 = {
        '04': (0, 1),  '05': (1, 1),  '06': (2, 1),
        '07': (3, 1),  '08': (4, 1),  '09': (5, 1),
        '10': (6, 1),  '11': (7, 1),  '12': (8, 1),
        '01': (9, 0),  '02': (10, 0), '03': (11, 0)
    }
    month0, year_add = MONTHS0[month]
    fyear = year + year_add
    
    context = {
        "client": projects[0].cluster,
        "year": '%d/%d' % (fyear-1, fyear) if fyear else 'Unknown',
        "month": MONTHS[int(month)-1],

        ### Summary section
        "summary-progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation'])),
        "summary-projects-3months": len([p for p in projects if p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
        "summary-projects-accounts": len([p for p in projects if p.phase == 'final-accounts']),
        "summary-projects-completed": len([p for p in projects if p.phase == 'completed']),
        "summary-projects-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation'])
        ),
        "summary-projects-implementation": len([p for p in projects if p.phase == 'implementation']),
        "summary-projects-planning": len([p for p in projects if p.phase == 'planning']),
        "summary-projects-total": len([p for p in projects]),
        ###
        ### Planning section
        "planning-appointment": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'consultant-appointment']),
        "planning-completed": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'completed']),
        "planning-design": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'design-costing']),
        "planning-documentation": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'documentation']),
        "planning-tender": len([p for p in projects if p.phase == 'planning' and p.planning_phase == 'tender']),
        "planning-total": len([p for p in projects if p.phase == 'planning']),
        ###
        ### Programmes in planning section
        "programmes-planning": [
            {
                "name": programme,
                "completed": len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'completed']),
                "appointments": len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'consultant-appointment']),
                "design": len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'design-costing']),
                "documentation": len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'documentation']),
                "tender": len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'tender']),
                "total": len([p for p in projects if p.programme == programme and p.phase == 'planning']),
                "donut": {
                    "values": [ 
                        len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'completed']),
                        len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'consultant-appointment']),
                        len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'design-costing']),
                        len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'documentation']),
                        len([p for p in projects if p.programme == programme and p.phase == 'planning' and p.planning_phase == 'tender'])
                    ]
                },
            } for programme in programmes_planning if programme != '--------'
        ],
        ###
        ### Implementation section
        "implementation-3months": len([p for p in projects if p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
        "implementation-final": len([p for p in projects if p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
        "implementation-fy": len([p for p in projects if p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
        "implementation-month": len([p for p in projects if p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
        "implementation-practical": len([p for p in projects if p.phase == 'implementation' and p.implementation_phase ==  'practical-completion']),
        "implementation-total": len([p for p in projects if p.phase == 'implementation']),
        "implementation-donut": {
            "values": [
                len([p for p in projects if p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
                len([p for p in projects if p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
                len([p for p in projects if p.phase == 'implementation' and p.implementation_phase ==  'practical-completion']),
                len([p for p in projects if p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
                len([p for p in projects if p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
            ]
        },
        "implementation-progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation'])),
        "implementation-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation'])
        ),
        ###
        ### Programmes in implementation section
        "programmes-implementation": [
            {
                "name": programme,
                "projects-total": len([p for p in projects if p.programme == programme and p.phase == 'implementation']),
                "projects-0-50": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
                "projects-51-75": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
                "projects-76-99": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
                "projects-100": len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
                "projects-donut": build_donut([
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) <= 0.5]),
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.5 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.75]),
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and 0.75 < _safe_float(_progress_for_month(p.planning, month0)) <= 0.99]),
                    len([p for p in projects if p.programme == programme and p.phase == 'implementation' and _safe_float(_progress_for_month(p.planning, month0)) >= 1.0]),
                ]),
                "progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])),
                "progress-gauge": build_gauge(
                    _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.programme == programme and p.phase == 'implementation']),
                    _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])
                ),
            } for programme in programmes_implementation if programme != '--------'
        ],
        ###
        ### Projects for tender section
        "projects-tender": [
            {
                "name": p.name,
            } for p in projects if p.phase == 'planning' and p.planning_phase == 'tender'
        ],
        ###
        ### Projects completed for implementation section
        "projects-planning-completed": [
            {
                "name": p.name,
                "budget": _currency(p.total_anticipated_cost)
            } for p in projects if p.phase == 'planning' and p.planning_phase == 'completed'
        ],
        ###
        ### Completed projects section
        "projects-completed": [
            {
                "name": p.name,
                "budget": _currency(p.total_anticipated_cost)
            } for p in projects if p.phase == 'completed'
        ],
        ###
        ### District summary section
        "district-nkangala-projects-implementation": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation']),
        "district-nkangala-projects-due-fy": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
        "district-nkangala-projects-due-3months": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
        "district-nkangala-projects-due-month": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
        "district-nkangala-projects-practical": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and p.implementation_phase == 'practical-completion']),
        "district-nkangala-projects-final": len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
        "district-nkangala-projects-donut": build_donut([
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and p.implementation_phase == 'practical-completion']),
            len([p for p in projects if p.district == 'Nkangala' and p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
        ]),
        "district-nkangala-progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation' and p.district == 'Nkangala'])),
        "district-nkangala-progress-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation' and p.district == 'Nkangala']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation' and p.district == 'Nkangala'])
        ),
        
        "district-gertsibande-projects-implementation": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation']),
        "district-gertsibande-projects-due-fy": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
        "district-gertsibande-projects-due-3months": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
        "district-gertsibande-projects-due-month": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
        "district-gertsibande-projects-practical": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and p.implementation_phase == 'practical-completion']),
        "district-gertsibande-projects-final": len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
        "district-gertsibande-projects-donut": build_donut([
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and p.implementation_phase == 'practical-completion']),
            len([p for p in projects if p.district == 'Gert Sibande' and p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
        ]),
        "district-gertsibande-progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation' and p.district == 'Gert Sibande'])),
        "district-gertsibande-progress-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation' and p.district == 'Gert Sibande']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation' and p.district == 'Gert Sibande'])
        ),
        
        "district-ehlanzeni-projects-implementation": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation']),
        "district-ehlanzeni-projects-due-fy": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
        "district-ehlanzeni-projects-due-3months": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
        "district-ehlanzeni-projects-due-month": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
        "district-ehlanzeni-projects-practical": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and p.implementation_phase == 'practical-completion']),
        "district-ehlanzeni-projects-final": len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
        "district-ehlanzeni-projects-donut": build_donut([
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _in_financial_year(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _in_3months(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and _in_month(p.planned_completion, year, month)]),
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and p.implementation_phase == 'practical-completion']),
            len([p for p in projects if p.district == 'Ehlanzeni' and p.phase == 'implementation' and p.implementation_phase == 'final-completion']),
        ]),
        "district-ehlanzeni-progress": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation' and p.district == 'Ehlanzeni'])),
        "district-ehlanzeni-progress-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation' and p.district == 'Ehlanzeni']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation' and p.district == 'Ehlanzeni'])
        ),
        ###
    }
    return HttpResponse(json.dumps(context), mimetype='application/json')

#@cache_page(settings.API_CACHE)
def cluster_performance_json(request, cluster, year=None, month=None):
    projects = filter(
        lambda x: x.cluster.lower().replace(' ', '-') == cluster,
        [Project.get(p) for p in Project.list() if p]
    )
    programmes = set([p.programme for p in projects])
    programmes_implementation = set([p.programme for p in projects if p.phase == 'implementation'])
    programmes_planning = set([p.programme for p in projects if p.phase == 'planning'])

    if not year or not month:
        timestamp = max([project.timestamp for project in projects])
        year = timestamp.year
        month = '%02d' % (timestamp.month)
    else:
        year = int(year)
        month = month
        
    # Convert month number to 0 indexed month.
    MONTHS0 = {
        '04': (0, 1),  '05': (1, 1),  '06': (2, 1),
        '07': (3, 1),  '08': (4, 1),  '09': (5, 1),
        '10': (6, 1),  '11': (7, 1),  '12': (8, 1),
        '01': (9, 0),  '02': (10, 0), '03': (11, 0)
    }
    month0, year_add = MONTHS0[month]
    fyear = year + year_add
    
    context = {
        "client": projects[0].cluster,
        "year": '%d/%d' % (fyear-1, fyear) if fyear else 'Unknown',
        "month": MONTHS[int(month)-1],

        ### Summary section
        "summary-projects-total": len([p for p in projects]),
        "summary-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects])),
        "summary-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects])),
        "summary-under-expenditure": _currency(
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects]) -
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects])
        ),
        "summary-budget-planning": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'planning'])),
        "summary-budget-implementation": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'implementation'])),
        "summary-budget-final-accounts": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'final-accounts'])),
        "summary-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects]),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects])
        ),
        ###
        ### Planning section
        "planning-projects-total": len([p for p in projects if p.phase == 'planning']),
        "planning-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'planning'])),
        "planning-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'planning'])),
        "planning-under-expenditure": _currency(
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'planning']) -
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'planning'])
        ),
        "planning-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'planning']),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'planning'])
        ),
        ###
        ### Programmes in planning section
        "programmes-planning": [
            {
                "name": programme,
                "projects-total": len([p for p in projects if p.programme == programme and p.phase == 'planning']),
                "budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme and p.phase == 'planning'])),
                "expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme and p.phase == 'planning'])),
                "under-expenditure": _currency(
                    sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme and p.phase == 'planning']) -
                    sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme and p.phase == 'planning'])
                ),
                "budget-slider": build_slider(
                    sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme and p.phase == 'planning']),
                    sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme and p.phase == 'planning'])
                ),
            } for programme in programmes_planning if programme != '--------'
        ],
        ###
        ### Implementation section
        "implementation-projects-total": len([p for p in projects if p.phase == 'implementation']),
        "implementation-budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'implementation'])),
        "implementation-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'implementation'])),
        "implementation-under-expenditure": _currency(
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'implementation']) -
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'implementation'])
        ),
        "implementation-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.phase == 'implementation']),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.phase == 'implementation'])
        ),
        ###
        ### Programmes in implementation section
        "programmes-implementation": [
            {
                "name": programme,
                "projects-total": len([p for p in projects if p.programme == programme and p.phase == 'implementation']),
                "budget": _currency(sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])),
                "expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])),
                "under-expenditure": _currency(
                    sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme and p.phase == 'implementation']) -
                    sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])
                ),
                "budget-slider": build_slider(
                    sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme and p.phase == 'implementation']),
                    sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])
                ),
            } for programme in programmes_implementation if programme != '--------'
        ],
        ###
        ### Overall analysis section
        "analysis-overall-expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects])),
        "analysis-overall-performance": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.phase == 'implementation'])),
        "analysis-overall-progress-gauge": build_gauge(
            _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.phase == 'implementation']),
            _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.phase == 'implementation'])
        ),
        "analysis-overall-budget-slider": build_slider(
            sum([_safe_float(p.expenditure_to_date) or 0 for p in projects]),
            sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects])
        ),
        ###
        ### Programme analysis section
        "programmes-analysis": [
            {
                "name": programme,
                "expenditure": _currency(sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme])),
                "performance": _percent(_avg([_safe_float(_progress_for_month(p.actual, month0)) or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])),
                "progress-gauge": build_gauge(
                    _avg([_safe_float(_progress_for_month(p.planning, month0))*100 or 0 for p in projects if p.programme == programme and p.phase == 'implementation']),
                    _avg([_safe_float(_progress_for_month(p.actual, month0))*100 or 0 for p in projects if p.programme == programme and p.phase == 'implementation'])
                ),
                "budget-slider": build_slider(
                    sum([_safe_float(p.expenditure_to_date) or 0 for p in projects if p.programme == programme]),
                    sum([_safe_float(p.total_anticipated_cost) or 0 for p in projects if p.programme == programme])
                ),
            } for programme in programmes_implementation if programme != '--------'
        ],
        ###
    }
    return HttpResponse(json.dumps(context), mimetype='application/json')

