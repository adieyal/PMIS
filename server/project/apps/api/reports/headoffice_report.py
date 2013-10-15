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

def build_gauge(planned, actual):
    needles = []
    if abs(actual-planned) < 10:
        text1 = " "
    else:
        text1 = None
    needles.append({ "needle-style": "dashed", 
                     "position": planned/100.0, 
                     "text": text1 or "Planned" })
    needles.append({ "needle-color": [ "#86bf53", "#cce310" ], 
                     "needle-style": "plain", 
                     "position": actual/100.0, 
                     "text": "Actual" })
    return needles

def build_donut(*args):
    return { "as_percentage": False, 
             "values": args }

def department_json(dept, date):
    client = models.Client.objects.get(name__iexact=dept)
    projects = models.Project.objects.client(client)

    values = {
        "dept_id" : dept_map[dept],
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
        "department-%(dept_id)s-implementation-budget" % values: format.format_currency(projects.total_implementation_budget(date.year)),
        "department-%(dept_id)s-implementation-budget-slider" % values: build_slider(projects.total_expenditure(date),
                                                                                     projects.total_budget(date.year),
                                                                                     color[values['dept_id']]),
        "department-%(dept_id)s-implementation-expenditure" % values: format.format_currency(projects.fy.actual_expenditure(date)),
        "department-%(dept_id)s-implementation-pecent-expenditure" % values: expenditure_percent(projects.total_expenditure(date),
                                                                                                 projects.total_budget(date.year)),
        "department-%(dept_id)s-implementation-progress" % values: format.format_percentage(projects.average_actual_progress(date)), 
        "department-%(dept_id)s-implementation-progress-gauge" % values: build_gauge(projects.average_planned_progress(date),
                                                                                     projects.average_actual_progress(date)),
        "department-%(dept_id)s-jobs" % values: format.format_number(projects.total_jobs(date)),
        "department-%(dept_id)s-name" % values: values["client"], 
        "department-%(dept_id)s-planning-budget" % values: format.format_currency(projects.total_planning_budget(date.year)), 
        "department-%(dept_id)s-planning-budget-slider" % values: build_slider(0,
                                                                               projects.total_planning_budget(date.year),
                                                                               color[values['dept_id']]), 
        "department-%(dept_id)s-planning-expenditure" % values: format.format_currency(0), 
        "department-%(dept_id)s-planning-pecent-expenditure" % values: format.format_percentage(0), 
        "department-%(dept_id)s-projects-accounts" % values: projects.in_finalaccounts.count(),
        "department-%(dept_id)s-projects-budget" % values: format.format_currency(projects.total_budget(date.year)), 
        "department-%(dept_id)s-projects-budget-slider" % values: build_slider(projects.total_expenditure(date),
                                                                               projects.total_budget(date.year),
                                                                               color[values['dept_id']]),
        "department-%(dept_id)s-projects-completed" % values: projects.completed().count(), 
        "department-%(dept_id)s-projects-expenditure" % values: format.format_currency(projects.total_expenditure(date)), 
        "department-%(dept_id)s-projects-implementation" % values: projects.in_implementation.count(), 
        "department-%(dept_id)s-projects-pecent-expenditure" % values: expenditure_percent(projects.total_expenditure(date),
                                                                                           projects.total_budget(date.year)), 
        "department-%(dept_id)s-projects-planning" % values: projects.in_planning.count(), 
        "department-%(dept_id)s-projects-total" % values: projects.count(), 
    }

def district_json(district, date):
    projects = models.Project.objects.district(models.District.objects.get(name=district))
    
    values = {
        "district_id" : district_map[district]
    }

    return {
        "district-%(district_id)s-budget" % values: format.format_currency(projects.total_budget(date.year)), 
        "district-%(district_id)s-budget-slider" % values: build_slider(projects.total_expenditure(date),
                                                                        projects.total_budget(date.year),
                                                                        "#E6B744"), 
        "district-%(district_id)s-expenditure" % values: format.format_currency(projects.total_expenditure(date)), 
        "district-%(district_id)s-percent-expenditure" % values: expenditure_percent(projects.total_expenditure(date),
                                                                                     projects.total_budget(date.year)), 
        "district-%(district_id)s-progress" % values: format.format_percentage(projects.average_actual_progress(date)), 
        "district-%(district_id)s-progress-gauge" % values: build_gauge(projects.average_planned_progress(date),
                                                                        projects.average_actual_progress(date)), 
        "district-%(district_id)s-projects-completed" % values: projects.completed().count(), 
        "district-%(district_id)s-projects-implementation" % values: projects.in_implementation.count(), 
        "district-%(district_id)s-projects-planning" % values: projects.in_planning.count(), 
        "district-%(district_id)s-projects-total" % values: projects.count(), 
    }
    

@cache_page(settings.API_CACHE)
def headoffice_dashboard(request, year, month):
    year, month = int(year), int(month)
    date = datetime(year, month, 1)

    js = OrderedDict()
    js.update(department_json("dcsr", date))
    js.update(department_json("dedet", date))
    js.update(department_json("doe", date))
    js.update(department_json("doh", date))
    js.update(department_json("dsd", date))
    js.update(department_json("dssl", date))
    js.update(district_json("Nkangala", date))
    js.update(district_json("Gert Sibande", date))
    js.update(district_json("Ehlanzeni", date))

    response = common.JsonResponse(js)
    return response

def progress_summary_json(dept, date):
    client = models.Client.objects.get(name__iexact=dept)
    projects = models.Project.objects.client(client)
    
    return {
        "summary-overall-progress": format.format_percentage(projects.average_actual_progress(date)), 
        "summary-overall-progress-gauge": build_gauge(projects.average_planned_progress(date),
                                                      projects.average_actual_progress(date)), 
        "summary-project-status-donut": build_donut(projects.completed().count(),
                                                    projects.in_implementation.count(),
                                                    projects.due_in_3_months(date).count(),
                                                    projects.in_finalaccounts.count(),
                                                    projects.in_planning.count()), 
        "summary-projects-3months": projects.due_in_3_months(date).count(), 
        "summary-projects-accounts": projects.in_finalaccounts.count(), 
        "summary-projects-completed": projects.completed().count(), 
        "summary-projects-implementation": projects.in_implementation.count(), 
        "summary-projects-planning": projects.in_planning.count(), 
        "summary-projects-total": projects.count()
        }

def progress_planning_json(dept, date):
    client = models.Client.objects.get(name__iexact=dept)
    projects = models.Project.objects.client(client).in_planning

    def grab_name(l, x):
        try:
            return l[x].name
        except IndexError:
            return ""
    
    return {
        "planning-project-status-donut": build_donut(projects.filter(current_step__name="Planning Complete").count(),
                                                     projects.filter(current_step__name="Consultant Appointment").count(),
                                                     projects.filter(current_step__name="Design and Costing").count(),
                                                     projects.filter(current_step__name="Documentation").count(),
                                                     projects.filter(current_step__name="Tendering").count()),
        "planning-projects-appointments": projects.filter(current_step__name="Consultant Appointment").count(), 
        "planning-projects-completed": projects.filter(current_step__name="Planning Complete").count(), 
        "planning-projects-design": projects.filter(current_step__name="Design and Costing").count(), 
        "planning-projects-documentation": projects.filter(current_step__name="Documentation").count(), 
        "planning-projects-implementation-a": grab_name(projects.filter(current_step__name="Planning Complete"), 0), 
        "planning-projects-implementation-b": grab_name(projects.filter(current_step__name="Planning Complete"), 1),
        "planning-projects-implementation-c": grab_name(projects.filter(current_step__name="Planning Complete"), 2),
        "planning-projects-implementation-d": grab_name(projects.filter(current_step__name="Planning Complete"), 3),
        "planning-projects-implementation-e": grab_name(projects.filter(current_step__name="Planning Complete"), 4),
        "planning-projects-implementation-f": grab_name(projects.filter(current_step__name="Planning Complete"), 5),
        "planning-projects-implementation-g": grab_name(projects.filter(current_step__name="Planning Complete"), 6),
        "planning-projects-tender": projects.filter(current_step__name="Tendering").count(), 
        "planning-projects-tender-a": grab_name(projects.filter(current_step__name="Tendering"), 0), 
        "planning-projects-tender-b": grab_name(projects.filter(current_step__name="Tendering"), 1), 
        "planning-projects-tender-c": grab_name(projects.filter(current_step__name="Tendering"), 2), 
        "planning-projects-tender-d": grab_name(projects.filter(current_step__name="Tendering"), 3), 
        "planning-projects-tender-e": grab_name(projects.filter(current_step__name="Tendering"), 4), 
        "planning-projects-tender-f": grab_name(projects.filter(current_step__name="Tendering"), 5), 
        "planning-projects-tender-g": grab_name(projects.filter(current_step__name="Tendering"), 6), 
        "planning-projects-total": projects.count()
        }

def progress_implementation_json(dept, date):
    client = models.Client.objects.get(name__iexact=dept)
    projects = models.Project.objects.client(client).in_implementation

    return {
        "implemenatation-projects-due-financial-year": projects.completed_by_fye(date.year).count(), 
        "implemenatation-projects-due-month": projects.due_in_1_month(date).count(), 
        "implemenatation-projects-final-completion": projects.filter(current_step__name="Final Completion").count(), 
        "implemenatation-projects-implementation": projects.count(), 
        "implemenatation-projects-practical-completion": projects.filter(current_step__name="Practical Completion").count(), 
        "implemenatation-projects-progress": format.format_percentage(projects.average_actual_progress(date)), 
        "implemenatation-projects-status-donut": build_donut(projects.completed_by_fye(date.year).count(),
                                                             projects.due_in_1_month(date).count(),
                                                             projects.filter(current_step__name="Practical Completion").count(),
                                                             projects.filter(current_step__name="Final Completion").count()),
        "implemenatation-projects-total": projects.count()
        }

def progress_district_json(dept, district, date):
    projects = models.Project.objects.district(models.District.objects.get(name=district))
    
    values = {
        "district_id" : district_map[district]
    }

    return {
        "district-%(district_id)s-completion-donut" % values: build_donut(projects.due_in_3_months(date).count(), 
                                                                          projects.filter(current_step__name="Practical Completion").count(), 
                                                                          projects.completed_by_fye(date.year).count(), 
                                                                          projects.filter(current_step__name="Final Completion").count()),
        "district-%(district_id)s-progress" % values: format.format_percentage(projects.average_actual_progress(date)),
        "district-%(district_id)s-progress-gauge" % values: build_gauge(projects.average_planned_progress(date),
                                                                        projects.average_actual_progress(date)), 
        "district-%(district_id)s-projects-3months" % values: projects.due_in_3_months(date).count(), 
        "district-%(district_id)s-projects-final-completion" % values: projects.filter(current_step__name="Final Completion").count(), 
        "district-%(district_id)s-projects-financial-year" % values: projects.completed_by_fye(date.year).count(), 
        "district-%(district_id)s-projects-practical-completion" % values: projects.filter(current_step__name="Practical Completion").count(), 
        "district-%(district_id)s-projects-this-month" % values: projects.due_in_1_month(date).count(), 
        "district-%(district_id)s-projects-total" % values: projects.count(),
        }

def progress_worst_json(dept, num, date):
    try:
        project = models.Project.objects.worst_performing(date, count=num+1)[num]
    except IndexError:
        return {}
    
    values = {
        'worst_id': ['a', 'b', 'c', 'd'][num]
        }

    return {
        "worst-%(worst_id)s-budget" % values: format.format_currency(project.total_budget(date.year)), 
        "worst-%(worst_id)s-consultant" % values: "-", 
        "worst-%(worst_id)s-contractor" % values: "-", 
        "worst-%(worst_id)s-coordinator" % values: "-", 
        "worst-%(worst_id)s-department" % values: project.programme.client.description, 
        "worst-%(worst_id)s-jobs" % values: project.jobs_created(date), 
        "worst-%(worst_id)s-location" % values: project.municipality.name, 
        "worst-%(worst_id)s-name" % values: project.name, 
        "worst-%(worst_id)s-progress" % values: format.format_percentage(project.actual_progress(date)), 
        "worst-%(worst_id)s-progress-slider" % values: build_slider(project.all(date).actual_expenditure, project.total_budget(date.year)),
        "worst-%(worst_id)s-reason" % values: "-"
        }

@cache_page(settings.API_CACHE)
def headoffice_progress(request, year, month):
    year, month = int(year), int(month)
    date = datetime(year, month, 1)
    
    department = "doh"

    js = OrderedDict()
    js.update(progress_summary_json(department, date))
    js.update(progress_planning_json(department, date))
    js.update(progress_implementation_json(department, date))
    js.update(progress_district_json(department, "Nkangala", date))
    js.update(progress_district_json(department, "Gert Sibande", date))
    js.update(progress_district_json(department, "Ehlanzeni", date))
    js.update(progress_worst_json(department, 0, date))
    js.update(progress_worst_json(department, 1, date))
    js.update(progress_worst_json(department, 2, date))
    js.update(progress_worst_json(department, 3, date))

    response = common.JsonResponse(js)
    return response

def performance_department_json(dept, date):
    client = models.Client.objects.get(name__iexact=dept)
    projects = models.Project.objects.client(client)

    values = {
        "dept_id" : dept_map[dept],
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
    
    def under_expenditure(budget, expenditure):
        try:
            under = (budget-expenditure)/budget
        except ZeroDivisionError:
            return "-"
        return format.format_percentage(under*100.0)

    return {
        "summary-department-%(dept_id)s-name" % values: values['client'], 
        "summary-department-%(dept_id)s-projects" % values: projects.count(), 
        "summary-department-%(dept_id)s-slider" % values: build_slider(projects.fy.total_expenditure(date),
                                                                       projects.fy.total_budget(date.year),
                                                                       color[values['dept_id']]),
        "summary-department-%(dept_id)s-under-expenditure" % values: under_expenditure(projects.fy.total_budget(date.year),
                                                                                       projects.fy.total_expenditure(date)),
        
        "summary-department-%(dept_id)s-budget" % values: format.format_currency(projects.fy.total_budget(date.year)), 
        "summary-department-%(dept_id)s-budget-final-accounts" % values: format.format_currency(0), 
        "summary-department-%(dept_id)s-budget-implementation" % values: format.format_currency(projects.fy.total_implementation_budget(date.year)), 
        "summary-department-%(dept_id)s-budget-planning" % values: format.format_currency(projects.fy.total_planning_budget(date.year)), 
        "summary-department-%(dept_id)s-expenditure" % values: format.format_currency(projects.fy.total_expenditure(date)), 

        "summary-department-%(dept_id)s-implementation-budget" % values: format.format_currency(projects.fy.total_implementation_budget(date.year)),  
        "summary-department-%(dept_id)s-implementation-expenditure" % values: "?",
        "summary-department-%(dept_id)s-implementation-projects" % values: projects.in_implementation.count(), 
        "summary-department-%(dept_id)s-implementation-slider" % values: [
            { "bar-color": color[values['dept_id']], 
              "marker-color": "#656263", 
              "marker-style": "short", 
              "marker-text": "Budget", 
              "position": 0.5 } 
            ], 
        "summary-department-%(dept_id)s-implementation-under-expenditure" % values: "?%", 

        "summary-department-%(dept_id)s-planning-budget" % values: format.format_currency(projects.fy.total_planning_budget(date.year)), 
        "summary-department-%(dept_id)s-planning-expenditure" % values: "?", 
        "summary-department-%(dept_id)s-planning-projects" % values: projects.in_planning.count(), 
        "summary-department-%(dept_id)s-planning-slider" % values: [
            { "bar-color": color[values['dept_id']], 
              "marker-color": "#656263", 
              "marker-style": "short", 
              "marker-text": "Budget", 
              "position": 0.5 }
            ], 
        "summary-department-%(dept_id)s-planning-under-expenditure" % values: "?%", 
        }

def performance_worst_json(num, date):
    try:
        project = models.Project.objects.worst_performing(date, count=num+1)[num]
    except IndexError:
        return {}
    
    values = {
        'worst_id': ['a', 'b', 'c', 'd', 'e', 'f'][num]
        }
    
    color = {
        "a": "#958BB7",
        "b": "#95CBEF",
        "c": "#85CABB",
        "d": "#E6B744",
        "e": "#B5B278",
        "f": "#BC6293"
        }
    
    def over_expenditure(budget, expenditure):
        try:
            under = (expenditure-budget)/budget
        except ZeroDivisionError:
            return "-"
        return format.format_percentage(under*100.0)

    return {
        "worst-%(worst_id)s-budget" % values: format.format_currency(project.total_budget(date.year)), 
        "worst-%(worst_id)s-department" % values: project.programme.client.description, 
        "worst-%(worst_id)s-expenditure" % values: format.format_currency(project.fy(date).actual_expenditure), 
        "worst-%(worst_id)s-location" % values: project.municipality.name, 
        "worst-%(worst_id)s-name" % values: project.name, 
        "worst-%(worst_id)s-over-expenditure" % values: format.format_currency(project.fy(date).actual_expenditure-project.total_budget(date.year)), 
        "worst-%(worst_id)s-over-expenditure-percent" % values: over_expenditure(project.total_budget(date.year),
                                                                                 project.fy(date).actual_expenditure), 
        "worst-%(worst_id)s-slider" % values: build_slider(project.all(date).actual_expenditure, project.total_budget(date.year), color[values['worst_id']])
        }

def performance_top_json(num, date):
    try:
        project = models.Project.objects.best_performing(date, count=num+1)[num]
    except IndexError:
        return {}
    
    values = {
        'top_id': ['a', 'b', 'c', 'd', 'e', 'f'][num]
        }
    
    color = {
        "a": "#958BB7",
        "b": "#95CBEF",
        "c": "#85CABB",
        "d": "#E6B744",
        "e": "#B5B278",
        "f": "#BC6293"
        }
    
    def over_expenditure(budget, expenditure):
        try:
            under = (expenditure-budget)/budget
        except ZeroDivisionError:
            return "-"
        return format.format_percentage(under*100.0)

    return {
        "top-%(top_id)s-budget" % values: format.format_currency(project.total_budget(date.year)), 
        "top-%(top_id)s-department" % values: project.programme.client.description, 
        "top-%(top_id)s-expenditure" % values: format.format_currency(project.fy(date).actual_expenditure), 
        "top-%(top_id)s-location" % values: project.municipality.name, 
        "top-%(top_id)s-name" % values: project.name, 
        "top-%(top_id)s-over-expenditure" % values: format.format_currency(project.fy(date).actual_expenditure-project.total_budget(date.year)), 
        "top-%(top_id)s-over-expenditure-percent" % values: over_expenditure(project.total_budget(date.year),
                                                                                 project.fy(date).actual_expenditure), 
        "top-%(top_id)s-slider" % values: build_slider(project.all(date).actual_expenditure, project.total_budget(date.year), color[values['top_id']])
        }

def performance_analysis_json(dept, date):
    client = models.Client.objects.get(name__iexact=dept)
    projects = models.Project.objects.client(client)

    values = {
        "dept_id" : dept_map[dept],
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
    
    def expenditure(budget, expenditure):
        try:
            return min((expenditure/budget)*100.0, 100)
        except ZeroDivisionError:
            return 100

    return {
        "analysis-department-%(dept_id)s-implementation-expenditure" % values: "%.2f%%" % expenditure(projects.fy.total_implementation_budget(date.year),
                                                                                                      projects.fy.total_expenditure(date)),
        "analysis-department-%(dept_id)s-implementation-gauge" % values: [], 
        "analysis-department-%(dept_id)s-implementation-performance" % values: "?%", 
        "analysis-department-%(dept_id)s-implementation-slider" % values: [
            { "bar-color": color[values['dept_id']], 
              "marker-color": color[values['dept_id']], 
              "marker-style": "long", 
              "marker-text": "Expenditure", 
              "position": expenditure(projects.fy.total_implementation_budget(date.year), projects.fy.total_expenditure(date))/100.0 }
            ], 
        
        "analysis-department-%(dept_id)s-name" % values: values['client'],
        "analysis-department-%(dept_id)s-overall-expenditure" % values: "%.2f%%" % expenditure(projects.fy.total_budget(date.year),
                                                                                               projects.fy.total_expenditure(date)), 
        "analysis-department-%(dept_id)s-overall-gauge" % values: [
            { "needle-color": [ "#86bf53", "#cce310" ], 
              "needle-style": "plain", 
              "position": (projects.average_performance(date) or 0), 
              "text": "Actual"
              }
            ], 
        "analysis-department-%(dept_id)s-overall-performance" % values: "%.2f%%" % ((projects.average_performance(date) or 0)*100), 
        "analysis-department-%(dept_id)s-overall-slider" % values: [
            { "bar-color": color[values['dept_id']], 
              "marker-color": color[values['dept_id']], 
              "marker-style": "long", 
              "marker-text": "Expenditure", 
              "position": expenditure(projects.fy.total_budget(date.year), projects.fy.total_expenditure(date))/100.0 }
            ],
        
        "analysis-department-%(dept_id)s-planning-expenditure" % values: "0%", 
        "analysis-department-%(dept_id)s-planning-gauge" % values: [], 
        "analysis-department-%(dept_id)s-planning-performance" % values: "?%", 
        "analysis-department-%(dept_id)s-planning-slider" % values: [
            { "bar-color": color[values['dept_id']], 
              "marker-color": color[values['dept_id']], 
              "marker-style": "long", 
              "marker-text": "Expenditure", 
              "position": 0 }
            ]
        }

@cache_page(settings.API_CACHE)
def headoffice_performance(request, year, month):
    year, month = int(year), int(month)
    date = datetime(year, month, 1)

    js = OrderedDict()
    js.update(performance_department_json("dcsr", date))
    js.update(performance_department_json("dedet", date))
    js.update(performance_department_json("doe", date))
    js.update(performance_department_json("doh", date))
    js.update(performance_department_json("dsd", date))
    js.update(performance_department_json("dssl", date))
    js.update(performance_worst_json(0, date))
    js.update(performance_worst_json(1, date))
    js.update(performance_worst_json(2, date))
    js.update(performance_worst_json(3, date))
    js.update(performance_worst_json(4, date))
    js.update(performance_worst_json(5, date))
    js.update(performance_top_json(0, date))
    js.update(performance_top_json(1, date))
    js.update(performance_top_json(2, date))
    js.update(performance_top_json(3, date))
    js.update(performance_top_json(4, date))
    js.update(performance_top_json(5, date))
    js.update(performance_analysis_json("dcsr", date))
    js.update(performance_analysis_json("dedet", date))
    js.update(performance_analysis_json("doe", date))
    js.update(performance_analysis_json("doh", date))
    js.update(performance_analysis_json("dsd", date))
    js.update(performance_analysis_json("dssl", date))

    response = common.JsonResponse(js)
    return response

