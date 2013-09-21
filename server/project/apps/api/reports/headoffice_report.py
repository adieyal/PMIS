from __future__ import division
from datetime import datetime
from collections import OrderedDict

from project.apps.projects import models
import common
import format

dept_map = {
    "dcsr" : "a", "dedet" : "b",
    "doe" : "c", "doh" : "d",
    "dsd" : "e", "dssl" : "f",
}

district_map = {
    "nkangala" : "a",
    "gert sibande" : "b",
    "ehlanzeni" : "c",
}

def department_json(dept, date):
    client = models.Client.objects.get(name__iexact=dept)
    projects = models.Project.objects.client(client)

    values = {
        "dept_id" : dept_map[dept],
        "client" : client.description,
    }

    return {
        "department-%(dept_id)s-implementation-budget" % values: format.format_currency(projects.total_budget()),
        "department-%(dept_id)s-implementation-budget-slider" % values: [
            {
                "bar-color": "#e5b744", 
                "marker-color": "#656263", 
                "marker-style": "short", 
                "marker-text": "Budget", 
                "position": 0.5
            }, 
            {
                "bar-color": "#f04338", 
                "marker-color": "#f04338", 
                "marker-style": "long", 
                "marker-text": "Actual", 
                "position": 0.65
            }
        ], 
        "department-%(dept_id)s-implementation-expenditure" % values: format.format_currency(projects.fy.actual_expenditure(date)),
        "department-%(dept_id)s-implementation-pecent-expenditure" % values: format.format_percentage(projects.fy.percentage_actual_expenditure(date)),
        "department-%(dept_id)s-implementation-progress" % values: format.format_percentage(projects.average_actual_progress(date)), 
        "department-%(dept_id)s-implementation-progress-gauge" % values: [
            {
                "needle-style": "dashed", 
                "position": 0.5, 
                "text": "Planned"
            }, 
            {
                "needle-color": [
                    "#86bf53", 
                    "#cce310"
                ], 
                "needle-style": "plain", 
                "position": 0.85, 
                "text": "Actual"
            }
        ], 
        "department-%(dept_id)s-jobs" % values: format.format_number(projects.total_jobs(date)),
        "department-%(dept_id)s-name" % values: values["client"], 
        "department-%(dept_id)s-planning-budget" % values: "R800,000", 
        "department-%(dept_id)s-planning-budget-slider" % values: [
            {
                "bar-color": "#e5b744", 
                "marker-color": "#656263", 
                "marker-style": "short", 
                "marker-text": "Budget", 
                "position": 0.5
            }, 
            {
                "bar-color": "#f04338", 
                "marker-color": "#f04338", 
                "marker-style": "long", 
                "marker-text": "Actual", 
                "position": 0.65
            }
        ], 
        "department-%(dept_id)s-planning-expenditure" % values: "R800,000", 
        "department-%(dept_id)s-planning-pecent-expenditure" % values: "30%", 
        "department-%(dept_id)s-projects-accounts" % values: "4", 
        "department-%(dept_id)s-projects-budget" % values: "R800,000", 
        "department-%(dept_id)s-projects-budget-slider" % values: [
            {
                "bar-color": "#e5b744", 
                "marker-color": "#656263", 
                "marker-style": "short", 
                "marker-text": "Budget", 
                "position": 0.5
            }, 
            {
                "bar-color": "#f04338", 
                "marker-color": "#f04338", 
                "marker-style": "long", 
                "marker-text": "Actual", 
                "position": 0.65
            }
        ], 
        "department-%(dept_id)s-projects-completed" % values: "5", 
        "department-%(dept_id)s-projects-expenditure" % values: "R800,000", 
        "department-%(dept_id)s-projects-implementation" % values: "40", 
        "department-%(dept_id)s-projects-pecent-expenditure" % values: "30%", 
        "department-%(dept_id)s-projects-planning" % values: "5", 
        "department-%(dept_id)s-projects-total" % values: "20", 
    }

def district_json(district):
    values = {
        "district_id" : district_map[district]
    }
    return {
        "district-%(district_id)s-budget": "R800,000", 
        "district-%(district_id)s-budget-slider": [
            {
                "bar-color": "#e5b744", 
                "marker-color": "#656263", 
                "marker-style": "short", 
                "marker-text": "Budget", 
                "position": 0.5
            }, 
            {
                "bar-color": "#f04338", 
                "marker-color": "#f04338", 
                "marker-style": "long", 
                "marker-text": "Actual", 
                "position": 0.65
            }
        ], 
        "district-%(district_id)s-expenditure": "R800,000", 
        "district-%(district_id)s-percent-expenditure": "30%", 
        "district-%(district_id)s-progress": "70%", 
        "district-%(district_id)s-progress-gauge": [
            {
                "needle-style": "dashed", 
                "position": 0.5, 
                "text": "Planned"
            }, 
            {
                "needle-color": [
                    "#86bf53", 
                    "#cce310"
                ], 
                "needle-style": "plain", 
                "position": 0.85, 
                "text": "Actual"
            }
        ], 
        "district-%(district_id)s-projects-completed": "3", 
        "district-%(district_id)s-projects-implementation": "1", 
        "district-%(district_id)s-projects-planning": "5", 
        "district-%(district_id)s-projects-total": "5", 
    }
    

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
    js.update(district_json("nkangala"))
    js.update(district_json("gert sibande"))
    js.update(district_json("ehlanzeni"))

    response = common.JsonResponse(js)
    return response
