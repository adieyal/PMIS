from __future__ import division
from django.http import HttpResponse, Http404
from django.core.cache import cache
from collections import OrderedDict
from decimal import Decimal
from datetime import datetime
from django.shortcuts import get_object_or_404
import json
from django.db.models import Count
import project.apps.projects.models as models
import project.apps.api.serializers as serializers
from project.apps.api.reports import graphhelpers
from django.views.decorators.cache import cache_page
from django.conf import settings

"""
JSON views to product reports
"""

def avg(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)

def district_client_json(district, client, date):
    financial_year = models.FinancialYearManager.financial_year(date.year, date.month)

    projects = models.Project.objects.client(client).district(district)

    worst_performing = [
        serializers.expanded_project_serializer(project, date)
        for project in projects.worst_performing(date)
    ]

    return {
        "fullname" : client.description,
        "name" : client.name,
        "num_jobs" : 999,
        "total_budget" : float(projects.total_budget()),
        "overall_progress" : {
            "actual" : projects.average_actual_progress(date),
            "planned" : projects.average_planned_progress(date),
        },
        "overall_expenditure" : {
            "perc_expenditure" : projects.fy.percentage_actual_expenditure(date),
            "actual_expenditure" : projects.fy.actual_expenditure(date),
            "planned_expenditure" : projects.total_planned_expenditure(date),
        },
        "total_projects" : projects.count(),
        # TODO - might need to check project status - i.e. projects completed in previous financial years don't count
        "projects" : {
            "completed_in_fye" : len(projects.completed_by_fye(financial_year)),
            "currently_in_planning" : projects.in_planning.count(),
            "currently_in_implementation" : projects.in_implementation.count(),
            "currently_in_final_completion" : projects.in_finalcompletion.count(),
            "currently_in_practical_completion" : projects.in_practicalcompletion.count(),
            "between_0_and_50": projects.actual_progress_between(0, 50).count(),
            "between_51_and_75": projects.actual_progress_between(51, 75).count(),
            "between_76_and_99": projects.actual_progress_between(76, 99).count(),
            "due_in_3_months": projects.due_in_3_months(date).count(),
            "due_this_month": projects.due_in_1_month(date).count(),
            "worst_performing": worst_performing,
            "project_complete": projects.completed().count(),
        }
    }

def district_report_json(district_id, date):
    year = date.year
    month = date.month

    date = datetime(year, month, 1)

    district = get_object_or_404(models.District, pk=district_id)
    projects = models.Project.objects.district(district)
    best_projects = projects.best_performing(date, count=7)
    worst_projects = projects.worst_performing(date, count=7)
    js = {
        "date" : date,
        "district" : {
            "name" : district.name,
            "id" : district.id,
        },
        "clients" : [
            district_client_json(district, c, date) for c in models.Client.objects.all()
        ],
        "projects" : {
            "best_performing" : [
                serializers.expanded_project_serializer(project, date)
                for project in best_projects
            ],
            "worst_performing" : [
                serializers.expanded_project_serializer(project, date)
                for project in worst_projects
            ],
            "by_municipality" : {
                "count" : {
                    m.name : m.num_projects
                    for m in models.Municipality.objects.annotate(num_projects=Count('projects'))
                },
                "bad" : {
                    m.name : m.num_projects
                    for m in models.Municipality.objects.filter(
                        projects__in=projects.bad(date)
                    ).annotate(num_projects=Count('projects'))
                },
            }
        }
    }
    return js

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
    
@cache_page(settings.API_CACHE)
def district_report(request, district_id, year, month):
    year, month = int(year), int(month)
    js = district_report_json(district_id, datetime(year, month, 1))
    response = HttpResponse(json.dumps(js, cls=serializers.ModelEncoder, indent=4, default=handler), mimetype="application/json")
    return response

@cache_page(settings.API_CACHE)
def dashboard_graphs(request, district_id, year, month):

    def create_gauges(client):
        val1 = client["overall_progress"]["planned"] / 100.
        val2 = client["overall_progress"]["actual"] / 100.

        return graphhelpers.dashboard_gauge(val1, val2)

    def create_expenditure_slider(planned, actual, budget, client):
        if budget == 0:
            return graphhelpers.dashboard_slider(0, 0, client, text1="Planned", text2="Actual")
        else:
            planned = planned / budget; actual = actual / budget
            return graphhelpers.dashboard_slider(planned, actual, client, text1="Planned", text2="Actual")

    def create_project_slider(project):
        val1 = project["expenditure"]["planned"]
        val2 = project["expenditure"]["actual"]
        budget = float(project["budget"])
        return create_expenditure_slider(val1, val2, budget, project["client"])

    def create_client_sliders(client):
        planned = client["overall_expenditure"]["planned_expenditure"]
        actual = client["overall_expenditure"]["actual_expenditure"]
        budget = client["total_budget"]
        return create_expenditure_slider(planned, actual, budget, client["name"])

    def create_project_progress_slider(project):
        planned = project["progress"]["planned"]
        actual = project["progress"]["actual"]
        m = max(planned, actual)
        if m == 0:
            return graphhelpers.dashboard_slider(0, 0, project["client"])
        else:
            planned, actual = planned / m, actual / m
            return graphhelpers.dashboard_slider(planned, actual, project["client"])

    year, month = int(year), int(month)
    data = district_report_json(district_id, datetime(year, month, 1))

    js = OrderedDict()
    for i, client in enumerate(data["clients"]):
        js["gauge%d" % (i + 1)] = create_gauges(client)
        js["client_slider%d" % (i + 1)] = create_client_sliders(client)
        js["stagespie%d" % (i + 1)] = 0

    for i, project in enumerate(data["projects"]["best_performing"]):
        js["best%d_expenditure" % (i + 1)] = create_project_slider(project)
        js["best%d_progress" % (i + 1)] = create_project_progress_slider(project)

    for i, project in enumerate(data["projects"]["worst_performing"]):
        js["worst%d_expenditure" % (i + 1)] = create_project_slider(project)
        js["worst%d_progress" % (i + 1)] = create_project_progress_slider(project)

    js["mpmap"] = data["projects"]["by_municipality"]["bad"]

    for i, client in enumerate(data["clients"]):
        for j, project in enumerate(client["projects"]["worst_performing"]):
            progress = project["progress"]["actual"] / 100 
            progress_text = "%s%%" % int(project["progress"]["actual"])
            slider = graphhelpers.single_value_slider(progress, client["name"], progress_text)
            js["client_%d_worst_%d" % (i, j)] = slider
        

    response = HttpResponse(json.dumps(js, indent=4), mimetype="application/json")
    return response

    
