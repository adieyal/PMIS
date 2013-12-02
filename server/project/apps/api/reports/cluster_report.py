from __future__ import division
from datetime import datetime
from collections import OrderedDict
from django.views.decorators.cache import cache_page
from django.conf import settings

from project.apps.projects import models
import common
import format

dept_map = {
    "dcsr" : "a", "dedet" : "b",
    "doe" : "c", "doh" : "d",
    "dsd" : "e", "dssl" : "f",
}

district_map = {
    "Nkangala" : "a",
    "Gert Sibande" : "b",
    "Ehlanzeni" : "c",
}

def expenditure_percent(expenditure, budget):
    try:
        return '%.2f%%' % ((expenditure/budget)*100)
    except ZeroDivisionError:
        return '-'

def under_expenditure(budget, expenditure):
    try:
        under = (budget-expenditure)/budget
    except ZeroDivisionError:
        return "-"
    return format.format_percentage(under*100.0)

def build_slider(expenditure, budget, color="#e5b744"):
    markers = []
    normalize = (expenditure+budget)/(2.0/1.1/2.0) or 1
    if budget and abs(expenditure-budget)/normalize < 0.1:
        text1 = " "
    elif budget == 0 and expenditure == 0:
        text1 = " "
    else:
        text1 = None
    if expenditure > budget:
        markers.append({ "bar-color": color, 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "position": budget/normalize })
        markers.append({ "bar-color": "#f04338", 
                         "marker-color": "#f04338", 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "position": expenditure/normalize })
    elif expenditure == budget:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual",
                         "position": expenditure/normalize })
        markers.append({ "bar-color": "#e5b744", 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "position": budget/normalize })
    else:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "position": expenditure/normalize })
        markers.append({ "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "position": budget/normalize })
    return markers

def build_gauge(planned, actual, text1=None, text2=None):
    needles = []
    if abs(actual-planned) < 10:
        text1 = " "
    needles.append({ "needle-style": "dashed", 
                     "position": planned/100.0, 
                     "text": text1 or "Planned" })
    needles.append({ "needle-color": [ "#86bf53", "#cce310" ], 
                     "needle-style": "plain", 
                     "position": actual/100.0, 
                     "text": text2 or "Actual" })
    return needles

def build_donut(*args):
    return { "as_percentage": False, 
             "values": args }


def date_json(date):
    end_year = models.FinancialYearManager.financial_year(date.year, date.month)
    start_year = end_year - 1 
    month = date.strftime("%b")
    return {
        "month" : month,
        "start_year" : start_year,
        "end_year" : end_year,
    }
def dashboard_summary_json(client, date):
    projects = models.Project.objects.client(client)

    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    color = {
        "a": "#E6B744",
        "b": "#85CABB",
        "c": "#958BB7",
        "d": "#95CBEF",
        "e": "#B5B278",
        "f": "#BC6293"
        }
     
    return { 
        "client" : client.description,
        "total-budget": format.format_currency(projects.total_budget(date.year)), 
        "total-budget-slider": build_slider(
            projects.total_expenditure(date),
            projects.total_budget(date.year),
            color[values['dept_id']]
        ),
        "total-expenditure": format.format_currency(projects.total_expenditure(date)), 
        "total-progress": format.format_percentage(projects.average_actual_progress(date)), 
        "total-progress-gauge": build_gauge(
            projects.average_planned_progress(date),
            projects.average_actual_progress(date)
         ),
        "total-projects": projects.count(), 
        "total-projects-accounts": projects.in_finalaccounts.count(), 
        "total-projects-implementation": projects.in_implementation.count(), 
        "total-projects-planning": projects.in_planning.count()
    }

def dashboard_programme_json(client, prog, date):
    programme = client.programmes.all()[prog]
    projects = models.Project.objects.client(client).programme(programme)

    values = {
        "prog_id" : ["a", "b", "c"][prog],
        "programme" : programme.name,
    }
    
    color = {
        "a": "#E6B744",
        "b": "#85CABB",
        "c": "#958BB7",
        "d": "#95CBEF",
        "e": "#B5B278",
        "f": "#BC6293"
        }
    
    return {
        "programme-%(prog_id)s-name" % values: values["programme"],
        "programme-%(prog_id)s-budget-slider" % values: build_slider(projects.total_expenditure(date),
                                                                     projects.total_budget(date.year),
                                                                     color[values['prog_id']]),
        "programme-%(prog_id)s-projects-accounts" % values: projects.in_finalaccounts.count(), 
        "programme-%(prog_id)s-projects-implementation" % values: projects.in_implementation.count(), 
        "programme-%(prog_id)s-projects-planning" % values: projects.in_planning.count(), 
        "programme-%(prog_id)s-projects-total" % values: projects.count(), 
        "programme-%(prog_id)s-total-expenditure" % values: format.format_currency(projects.total_expenditure(date))
        }

def dashboard_planning_json(client, date):
    projects = models.Project.objects.client(client).in_planning

    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    return {
        "planning-budget": format.format_currency(projects.total_budget(date.year)), 
        "planning-budget-slider": build_slider(projects.total_expenditure(date),
                                               projects.total_budget(date.year)),
        "planning-expenditure": format.format_currency(projects.total_expenditure(date)), 
        "planning-stages-donut": build_donut(projects.filter(current_step__name="Consultant Appointment").count(), 
                                             projects.filter(current_step__name="Design and Costing").count(), 
                                             projects.filter(current_step__name="Documentation").count(), 
                                             projects.filter(current_step__name="Tendering").count()),
        "planning-total": projects.count(), 
        }

def dashboard_implementation_json(client, date):
    projects = models.Project.objects.client(client).in_implementation

    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    return {
        "implementation-budget": format.format_currency(projects.total_budget(date.year)), 
        "implementation-budget-slider": build_slider(projects.total_expenditure(date),
                                                     projects.total_budget(date.year)),
        "implementation-expenditure": expenditure_percent(projects.total_expenditure(date),
                                                          projects.total_budget(date.year)), 
        "implementation-progress": format.format_percentage(projects.average_actual_progress(date)), 
        "implementation-progress-gauge": build_gauge(projects.average_planned_progress(date),
                                                     projects.average_actual_progress(date)),
        "implementation-projects-complete": projects.completed().count(), 
        "implementation-projects-due": projects.due_in_3_months(date).count(), 
        "implementation-projects-final-completion": projects.filter(current_step__name="Final Completion").count(), 
        "implementation-projects-practical-completion": projects.filter(current_step__name="Practical Completion").count(), 
        "implementation-projects-total": projects.count()
        }

def dashboard_programme_implementation_json(client, prog, date):
    programme = client.programmes.all()[prog]
    projects = models.Project.objects.client(client).programme(programme)

    values = {
        "prog_id" : ["a", "b", "c"][prog],
        "programme" : programme.name,
    }
    
    return {
        "programme-%(prog_id)s-implementation-name" % values: programme.name,
        "programme-%(prog_id)s-implementation-budget-slider" % values: build_slider(projects.total_expenditure(date),
                                                                                    projects.total_budget(date.year)),
        "programme-%(prog_id)s-implementation-projects" % values: projects.count(), 
        "programme-%(prog_id)s-implementation-projects-appointment" % values: projects.filter(current_step__name="Consultant Appointment").count(), 
        "programme-%(prog_id)s-implementation-projects-budget" % values: format.format_currency(projects.total_budget(date.year)), 
        "programme-%(prog_id)s-implementation-projects-design" % values: projects.filter(current_step__name="Design and Costing").count(), 
        "programme-%(prog_id)s-implementation-projects-documentation" % values: projects.filter(current_step__name="Documentation").count(), 
        "programme-%(prog_id)s-implementation-projects-expenditure" % values: format.format_currency(projects.total_expenditure(date)), 
        "programme-%(prog_id)s-implementation-projects-tendering" % values: projects.filter(current_step__name="Tendering").count(), 
        "programme-%(prog_id)s-implementation-stages-donut" % values: build_donut(
            projects.filter(current_step__name="Consultant Appointment").count(), 
            projects.filter(current_step__name="Design and Costing").count(), 
            projects.filter(current_step__name="Documentation").count(), 
            projects.filter(current_step__name="Tendering").count()),
        }

def dashboard_district_json(client, district, date):
    projects = models.Project.objects.district(models.District.objects.get(name=district))
    
    values = {
        "district_id" : district_map[district]
    }

    return {
        "district-%(district_id)s-budget" % values: format.format_currency(projects.total_budget(date.year)), 
        "district-%(district_id)s-budget-slider" % values: build_slider(projects.total_expenditure(date),
                                                                        projects.total_budget(date.year)),
        "district-%(district_id)s-expenditure" % values: format.format_currency(projects.total_expenditure(date)), 
        "district-%(district_id)s-projects-appointment" % values: projects.filter(current_step__name="Consultant Appointment").count(), 
        "district-%(district_id)s-projects-design" % values: projects.filter(current_step__name="Design and Costing").count(), 
        "district-%(district_id)s-projects-documentation" % values: projects.filter(current_step__name="Documentation").count(), 
        "district-%(district_id)s-projects-implementation" % values: projects.in_implementation.count(), 
        "district-%(district_id)s-projects-tendering" % values: projects.filter(current_step__name="Tendering").count(), 
        "district-%(district_id)s-stages-donut" % values: build_donut(
            projects.filter(current_step__name="Consultant Appointment").count(), 
            projects.filter(current_step__name="Design and Costing").count(), 
            projects.filter(current_step__name="Documentation").count(), 
            projects.filter(current_step__name="Tendering").count())
    }
    

@cache_page(settings.API_CACHE)
def cluster_dashboard(request, client_code, year, month):
    year, month = int(year), int(month)
    date = datetime(year, month, 1)
    
    client = models.Client.objects.by_code(client_code)

    js = OrderedDict()
    js.update(date_json(date))
    js.update(dashboard_summary_json(client, date))
    js.update(dashboard_programme_json(client, 0, date))
    js.update(dashboard_programme_json(client, 1, date))
    js.update(dashboard_programme_json(client, 2, date))
    js.update(dashboard_planning_json(client, date))
    js.update(dashboard_implementation_json(client, date))
    js.update(dashboard_programme_implementation_json(client, 0, date))
    js.update(dashboard_programme_implementation_json(client, 1, date))
    js.update(dashboard_programme_implementation_json(client, 2, date))
    js.update(dashboard_district_json(client, "Nkangala", date))
    js.update(dashboard_district_json(client, "Gert Sibande", date))
    js.update(dashboard_district_json(client, "Ehlanzeni", date))

    response = common.JsonResponse(js)
    
    return response

def progress_summary_json(client, date):
    projects = models.Project.objects.client(client)
    
    return {
        "client" : client.description,
        "summary-progress": format.format_percentage(projects.average_actual_progress(date)), 
        "summary-projects-3months": projects.due_in_3_months(date).count(), 
        "summary-projects-accounts": projects.in_finalaccounts.count(), 
        "summary-projects-completed": projects.completed().count(), 
        "summary-projects-gauge": build_gauge(projects.average_planned_progress(date),
                                              projects.average_actual_progress(date)), 
        "summary-projects-implementation": projects.in_implementation.count(), 
        "summary-projects-planning": projects.in_planning.count(), 
        "summary-projects-total": projects.count()
        }

def progress_planning_json(client, date):
    projects = models.Project.objects.client(client).in_planning
    
    return {
        "planning-appointment": projects.filter(current_step__name="Consultant Appointment").count(), 
        "planning-completed": projects.filter(current_step__name="Planning Complete").count(), 
        "planning-design": projects.filter(current_step__name="Design and Costing").count(), 
        "planning-documentation": projects.filter(current_step__name="Documentation").count(), 
        "planning-tender": projects.filter(current_step__name="Tendering").count(), 
        "planning-total": projects.count()
        }

def progress_planning_programme_json(client, prog, date):
    try:
        programme = client.programmes.all()[prog]
    except IndexError:
        return {}
    projects = models.Project.objects.client(client).programme(programme).in_planning

    values = {
        "prog_id" : ["a", "b", "c", "d", "e", "f"][prog],
        "programme" : programme.name,
    }
    
    return {
        "planning-programme-%(prog_id)s-appointments" % values: projects.filter(current_step__name="Consultant Appointment").count(), 
        "planning-programme-%(prog_id)s-completed" % values: projects.filter(current_step__name="Planning Complete").count(),
        "planning-programme-%(prog_id)s-design" % values: projects.filter(current_step__name="Design and Costing").count(), 
        "planning-programme-%(prog_id)s-documentation" % values: projects.filter(current_step__name="Documentation").count(), 
        "planning-programme-%(prog_id)s-donut" % values: build_donut(
            projects.filter(current_step__name="Planning Complete").count(),
            projects.filter(current_step__name="Consultant Appointment").count(),
            projects.filter(current_step__name="Design and Costing").count(),
            projects.filter(current_step__name="Documentation").count(),
            projects.filter(current_step__name="Tendering").count()
            ),
        "planning-programme-%(prog_id)s-name" % values: programme.name, 
        "planning-programme-%(prog_id)s-tender" % values: projects.filter(current_step__name="Tendering").count(), 
        "planning-programme-%(prog_id)s-total" % values: projects.count()
        }

def progress_for_implementation_json(client, date):
    projects = models.Project.objects.client(client).in_planning.filter(current_step__name="Planning Complete")[0:15]

    response = {}
    for i, p in enumerate(projects):
        response["for-implementation-project-%s-name" % ('abcdefghijklmnop'[i])] = p.name
    return response

def progress_for_tender_json(client, date):
    projects = models.Project.objects.client(client).in_planning.filter(current_step__name="Tendering")[0:15]

    response = {}
    for i, p in enumerate(projects):
        response["for-tender-project-%s-name" % ('abcdefghijklmnop'[i])] = p.name
    return response

def progress_implementation_json(client, date):
    projects = models.Project.objects.client(client).in_implementation

    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    return {
        "implementation-3months": projects.due_in_3_months(date).count(), 
        "implementation-completion-percent": "%.2f%%" % (projects.filter(current_step__name="Final Completion").count()/float(projects.count())*100), 
        "implementation-progress-percent": format.format_percentage(projects.average_actual_progress(date)),
        "implementation-donut": build_donut(
            projects.completed_by_fye(date.year).count(),
            projects.due_in_3_months(date).count(),
            projects.filter(current_step__name="Practical Completion").count(),
            projects.filter(current_step__name="Final Completion").count(),
            projects.due_in_1_month(date).count(),
            ),
        "implementation-final": projects.filter(current_step__name="Final Completion").count(),
        "implementation-fy": projects.completed_by_fye(date.year).count(),
        "implementation-gauge": build_gauge(projects.average_planned_progress(date),
                                            projects.average_actual_progress(date)), 
        "implementation-month": projects.due_in_1_month(date).count(),
        "implementation-practical": projects.filter(current_step__name="Practical Completion").count(),
        "implementation-total": projects.count()
        
        }

def progress_implementation_programme_json(client, prog, date):
    try:
        programme = client.programmes.all()[prog]
    except IndexError:
        return {}
    projects = models.Project.objects.client(client).programme(programme).in_implementation

    values = {
        "prog_id" : ["a", "b", "c"][prog],
        "programme" : programme.name,
    }
    
    return {
        "implementation-programme-%(prog_id)s-appointments" % values: projects.filter(current_step__name="Consultant Appointment").count(), 
        "implementation-programme-%(prog_id)s-completed" % values: projects.filter(current_step__name="Planning Complete").count(),
        "implementation-programme-%(prog_id)s-design" % values: projects.filter(current_step__name="Design and Costing").count(), 
        "implementation-programme-%(prog_id)s-documentation" % values: projects.filter(current_step__name="Documentation").count(), 
        "implementation-programme-%(prog_id)s-donut" % values: build_donut(
            projects.filter(current_step__name="Planning Complete").count(),
            projects.filter(current_step__name="Consultant Appointment").count(), 
            projects.filter(current_step__name="Design and Costing").count(), 
            projects.filter(current_step__name="Documentation").count(), 
            projects.filter(current_step__name="Tendering").count()
            ), 
        "implementation-programme-%(prog_id)s-gauge" % values: build_gauge(projects.average_planned_progress(date),
                                                                           projects.average_actual_progress(date)), 
        "implementation-programme-%(prog_id)s-name" % values: programme.name, 
        "implementation-programme-%(prog_id)s-progress" % values: format.format_percentage(projects.average_actual_progress(date)),
        "implementation-programme-%(prog_id)s-tender" % values: projects.filter(current_step__name="Tendering").count(), 
        "implementation-programme-%(prog_id)s-total" % values: projects.count()
        }

def progress_district_json(client, district, date):
    projects = models.Project.objects.district(models.District.objects.get(name=district))
    
    values = {
        "district_id" : district_map[district]
    }

    return {
        "district-%(district_id)s-3months" % values: projects.due_in_3_months(date).count(), 
        "district-%(district_id)s-donut" % values: build_donut(
            projects.completed_by_fye(date.year).count(),
            projects.due_in_3_months(date).count(), 
            projects.due_in_1_month(date).count(),
            projects.filter(current_step__name="Practical Completion").count(),
            projects.filter(current_step__name="Final Completion").count(),
            projects.in_implementation.count()
            ),
        "district-%(district_id)s-final" % values: projects.filter(current_step__name="Final Completion").count(),
        "district-%(district_id)s-fy" % values: projects.completed_by_fye(date.year).count(),
        "district-%(district_id)s-gauge" % values: build_gauge(projects.average_planned_progress(date),
                                                               projects.average_actual_progress(date)), 
        "district-%(district_id)s-month" % values: projects.due_in_1_month(date).count(),
        "district-%(district_id)s-practical" % values: projects.filter(current_step__name="Practical Completion").count(),
        "district-%(district_id)s-progress" % values: format.format_percentage(projects.average_actual_progress(date)),
        "district-%(district_id)s-implementation" % values: projects.in_implementation.count()
        }

@cache_page(settings.API_CACHE)
def cluster_progress(request, client_code, year, month):
    year, month = int(year), int(month)
    date = datetime(year, month, 1)
    client = models.Client.objects.by_code(client_code)
    
    js = OrderedDict() 
    js.update(progress_summary_json(client, date))
    js.update(date_json(date))
    js.update(progress_planning_json(client, date))
    js.update(progress_planning_programme_json(client, 0, date))
    js.update(progress_planning_programme_json(client, 1, date))
    js.update(progress_planning_programme_json(client, 2, date))
    js.update(progress_planning_programme_json(client, 3, date))
    js.update(progress_planning_programme_json(client, 4, date))
    js.update(progress_planning_programme_json(client, 5, date))
    js.update(progress_for_tender_json(client, date))
    js.update(progress_for_implementation_json(client, date))
    js.update(progress_implementation_json(client, date))
    js.update(progress_implementation_programme_json(client, 0, date))
    js.update(progress_implementation_programme_json(client, 1, date))
    js.update(progress_implementation_programme_json(client, 2, date))
    js.update(progress_district_json(client, "Nkangala", date))
    js.update(progress_district_json(client, "Gert Sibande", date))
    js.update(progress_district_json(client, "Ehlanzeni", date))
    response = common.JsonResponse(js)
    return response  


def performance_summary_json(client, date):
    projects = models.Project.objects.client(client)

    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    color = {
        "a": "#E6B744",
        "b": "#85CABB",
        "c": "#958BB7",
        "d": "#95CBEF",
        "e": "#B5B278",
        "f": "#BC6293"
        }
    
    end_year = models.FinancialYearManager.financial_year(date.year, date.month)
    start_year = end_year - 1 
    month = date.strftime("%b")

    return {
        "client" : client.description,
        "month" : month,
        "start_year" : start_year,
        "end_year" : end_year,
        "summary-budget": format.format_currency(projects.total_budget(date.year)), 
        "summary-budget-final-accounts": "?", 
        "summary-budget-implementation": "?", 
        "summary-budget-planning": "?", 
        "summary-expenditure": format.format_currency(projects.total_expenditure(date)), 
        "summary-slider": build_slider(projects.total_expenditure(date),
                                       projects.total_budget(date.year)),
        "summary-total-projects": projects.count(), 
        "summary-under-expenditure": "%s (%s)" % (
            format.format_currency(projects.total_budget(date.year)-projects.total_expenditure(date)),
            under_expenditure(projects.total_budget(date.year),
            projects.total_expenditure(date))
        )    
    }

def performance_planning_json(client, date):
    projects = models.Project.objects.client(client).in_planning

    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    color = {
        "a": "#E6B744",
        "b": "#85CABB",
        "c": "#958BB7",
        "d": "#95CBEF",
        "e": "#B5B278",
        "f": "#BC6293"
        }
    
    return {
        "planning-total-budget": format.format_currency(projects.total_budget(date.year)), 
        "planning-expenditure": "%s (%s)" % (format.format_currency(projects.total_expenditure(date)),
                                             expenditure_percent(projects.total_budget(date.year),
                                                                 projects.total_expenditure(date))), 
        "planning-slider": build_slider(projects.total_expenditure(date),
                                        projects.total_budget(date.year)), 
        "planning-total-projects": projects.count(), 
        "planning-under-expenditure": "%s (%s)" % (format.format_currency(projects.total_budget(date.year)-projects.total_expenditure(date)),
                                                   under_expenditure(projects.total_budget(date.year),
                                                                     projects.total_expenditure(date)))
        }

def performance_planning_programmes_json(client, prog, date):
    programme = client.programmes.all()[prog]
    projects = models.Project.objects.client(client).programme(programme).in_planning

    values = {
        "prog_id" : ["a", "b", "c"][prog],
        "programme" : programme.name,
    }
    
    color = {
        "a": "#E6B744",
        "b": "#85CABB",
        "c": "#958BB7",
        "d": "#95CBEF",
        "e": "#B5B278",
        "f": "#BC6293"
        }
    
    return {
        "planning-programme-%(prog_id)s-name" % values: programme.name,
        "planning-programme-%(prog_id)s-budget" % values: format.format_currency(projects.total_budget(date.year)), 
        "planning-programme-%(prog_id)s-projects" % values: projects.count(), 
        "planning-programme-%(prog_id)s-slider" % values: build_slider(projects.total_expenditure(date),
                                                                       projects.total_budget(date.year),
                                                                       color[values['prog_id']]), 
        "planning-programme-%(prog_id)s-total-expenditure" % values: "%s (%s)" % (format.format_currency(projects.total_expenditure(date)),
                                                                                  expenditure_percent(projects.total_budget(date.year),
                                                                                                      projects.total_expenditure(date))), 
        "planning-programme-%(prog_id)s-under-expenditure" % values: "%s (%s)" % (format.format_currency(projects.total_budget(date.year)-projects.total_expenditure(date)),
                                                                                  under_expenditure(projects.total_budget(date.year),
                                                                                                    projects.total_expenditure(date))) 
        }

def performance_implementation_json(client, date):
    projects = models.Project.objects.client(client).in_implementation
    
    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    return {
        "implementation-budget": format.format_currency(projects.total_budget(date.year)), 
        "implementation-projects": projects.count(), 
        "implementation-slider": build_slider(projects.total_expenditure(date),
                                              projects.total_budget(date.year)),
        "implementation-total-expenditure": "%s (%s)" % (format.format_currency(projects.total_expenditure(date)),
                                                         expenditure_percent(projects.total_budget(date.year),
                                                                             projects.total_expenditure(date))), 
        "implementation-under-expenditure": "%s (%s)" % (format.format_currency(projects.total_budget(date.year)-projects.total_expenditure(date)),
                                                         under_expenditure(projects.total_budget(date.year),
                                                                           projects.total_expenditure(date)))
        }

def performance_implementation_programmes_json(client, prog, date):
    programme = client.programmes.all()[prog]
    projects = models.Project.objects.client(client).programme(programme).in_planning

    values = {
        "prog_id" : ["a", "b", "c"][prog],
        "programme" : programme.name,
    }
    
    color = {
        "a": "#E6B744",
        "b": "#85CABB",
        "c": "#958BB7",
        "d": "#95CBEF",
        "e": "#B5B278",
        "f": "#BC6293"
        }
    
    return {
        "implementation-programme-%(prog_id)s-name" % values: programme.name,
        "implementation-programme-%(prog_id)s-budget" % values: format.format_currency(projects.total_budget(date.year)), 
        "implementation-programme-%(prog_id)s-projects" % values: projects.count(), 
        "implementation-programme-%(prog_id)s-slider" % values: build_slider(projects.total_expenditure(date),
                                                                             projects.total_budget(date.year),
                                                                             color[values['prog_id']]), 
        "implementation-programme-%(prog_id)s-total-expenditure" % values: "%s (%s)" % (format.format_currency(projects.total_expenditure(date)),
                                                                                       expenditure_percent(projects.total_budget(date.year),
                                                                                                           projects.total_expenditure(date))), 
        "implementation-programme-%(prog_id)s-under-expenditure" % values: "%s (%s)" % (format.format_currency(projects.total_budget(date.year)-projects.total_expenditure(date)),
                                                                                        under_expenditure(projects.total_budget(date.year),
                                                                                                          projects.total_expenditure(date)))
        }

def performance_analysis_json(client, date):
    projects = models.Project.objects.client(client)
    
    values = {
        "dept_id" : dept_map[client.code.lower()],
        "client" : client.description,
    }
    
    return {
        "analysis-overall-expenditure": format.format_currency(projects.total_expenditure(date)), 
        "analysis-overall-expenditure-gauge": build_gauge(projects.average_planned_progress(date),
                                                          projects.average_actual_progress(date)),
        "analysis-overall-performace": "%.2f%%" % ((projects.average_performance(date) or 0)*100), 
        "analysis-overall-performance-slider": build_slider(projects.total_budget(date.year),
                                                            projects.total_expenditure(date))
        }

def performance_analysis_programmes_json(client, prog, date):
    programme = client.programmes.all()[prog]
    projects = models.Project.objects.client(client).programme(programme).in_planning

    values = {
        "prog_id" : ["a", "b", "c"][prog],
        "programme" : programme.name,
    }
    
    color = {
        "a": "#E6B744",
        "b": "#85CABB",
        "c": "#958BB7",
        "d": "#95CBEF",
        "e": "#B5B278",
        "f": "#BC6293"
        }

    return {
        "analysis-programme-%(prog_id)s-name" % values: programme.name,
        "analysis-programme-%(prog_id)s-expenditure" % values: format.format_currency(projects.total_expenditure(date)), 
        "analysis-programme-%(prog_id)s-expenditure-gauge" % values: build_gauge(projects.average_planned_progress(date),
                                                                                 projects.average_actual_progress(date)),
        "analysis-programme-%(prog_id)s-performace" % values: "%.2f%%" % ((projects.average_performance(date) or 0)*100), 
        "analysis-programme-%(prog_id)s-performance-slider" % values: build_slider(projects.total_budget(date.year),
                                                                                   projects.total_expenditure(date),
                                                                                   color[values['prog_id']])
        }

@cache_page(settings.API_CACHE)
def cluster_performance(request, client_code, year, month):
    year, month = int(year), int(month)
    date = datetime(year, month, 1)
    client = models.Client.objects.by_code(client_code)

    js = OrderedDict()
    js.update(performance_summary_json(client, date))
    js.update(date_json(date))
    js.update(performance_planning_json(client, date))
    js.update(performance_planning_programmes_json(client, 0, date))
    js.update(performance_planning_programmes_json(client, 1, date))
    js.update(performance_planning_programmes_json(client, 2, date))
    js.update(performance_implementation_json(client, date))
    js.update(performance_implementation_programmes_json(client, 0, date))
    js.update(performance_implementation_programmes_json(client, 1, date))
    js.update(performance_implementation_programmes_json(client, 2, date))
    js.update(performance_analysis_json(client, date))
    js.update(performance_analysis_programmes_json(client, 0, date))
    js.update(performance_analysis_programmes_json(client, 1, date))
    response = common.JsonResponse(js)
    return response

