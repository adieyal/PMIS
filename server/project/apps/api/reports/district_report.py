from django.http import HttpResponse, Http404
from django.core.cache import cache
from collections import OrderedDict
from decimal import Decimal
from datetime import datetime
from django.shortcuts import get_object_or_404
import json
import project.apps.projects.models as models
import project.apps.api.serializers as serializers
from project.apps.api.reports import graphhelpers

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
            "perc_expenditure" : projects.percentage_actual_expenditure(date) * 100,
            "actual_expenditure" : projects.total_actual_expenditure(date),
            "planned_expenditure" : projects.total_planned_expenditure(date),
        },
        "total_projects" : projects.count(),
        # TODO - might need to check project status - i.e. projects completed in previous financial years don't count
        "projects" : {
            "completed_in_fye" : len(projects.completed_by_fye(financial_year)),
            "currently_in_planning" : len(projects.filter(current_step__phase="planning")),
            "currently_in_implementation" : len(projects.filter(current_step__phase="implementation")),
            "currently_in_final_completion" : len(projects.filter(current_step=models.Milestone.final_accounts())),
            "currently_in_practical_completion" : len(projects.filter(current_step=models.Milestone.final_completion())),
            "between_0_and_50": len(projects.actual_progress_between(0, 50)),
            "between_51_and_75": len(projects.actual_progress_between(51, 75)),
            "between_76_and_99": len(projects.actual_progress_between(76, 99)),
            "due_in_3_months": 5,
            "due_this_month": 2,
        }
    }


def district_report_json(district_id, date):
    year = date.year
    month = date.month

    key = 'district_%s_%s_%s' % (district_id, year, month)
    js = cache.get(key)
    #if js: return js
        
    date = datetime(year, month, 1)

    district = get_object_or_404(models.District, pk=district_id)
    best_projects = models.Project.objects.district(district).best_performing(date, count=7)
    worst_projects = models.Project.objects.district(district).worst_performing(date, count=7)
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
        }
    }
    cache.set(key, js, 30)
    return js

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
    
def district_report(request, district_id, year, month):
    year, month = int(year), int(month)
    js = district_report_json(district_id, datetime(year, month, 1))
    return HttpResponse(json.dumps(js, cls=serializers.ModelEncoder, indent=4, default=handler), mimetype="application/json")


def dashboard_graphs(request, district_id, year, month):

    def create_gauges(client):
        val1 = client["overall_progress"]["planned"] / 100.
        val2 = client["overall_progress"]["actual"] / 100.

        return graphhelpers.dashboard_gauge(val1, val2)

    def create_client_sliders(client):
        val1 = client["overall_expenditure"]["planned_expenditure"]
        val2 = client["overall_expenditure"]["actual_expenditure"]
        budget = client["total_budget"]
        if client["total_budget"] == 0:
            return graphhelpers.dashboard_slider(0, 0, client["name"])
        else:
            val1 = val1 / budget; val2 = val2 / budget
            return graphhelpers.dashboard_slider(val1 / 10, val2 / 10, client["name"])

    year, month = int(year), int(month)
    data = district_report_json(district_id, datetime(year, month, 1))

    js = OrderedDict()
    for i, client in enumerate(data["clients"]):
        js["gauge%d" % (i + 1)] = create_gauges(client)
        js["slider%d" % (i + 1)] = create_client_sliders(client)

    return HttpResponse(json.dumps(js, indent=4), mimetype="application/json")

    
