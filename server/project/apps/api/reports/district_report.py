from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import json
import project.apps.projects.models as models

"""
JSON views to product reports
"""

def avg(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)

def district_client_json(district, client, year, month):
    #projects = models.Project.objects.filter(programme__client=client)
    project_financials = models.ProjectFinancial.objects.filter(
        project__programme__client=client, project__municipality__district=district
    )

    planning = models.Planning.objects.filter(
        project__programme__client=client, project__municipality__district=district,
        year=year, month=month
    )

    monthlysubmissions = models.MonthlySubmission.objects.filter(
        project__programme__client=client, project__municipality__district=district,
        year=year, month=month
    )

    return {
        "total_budget" : float(sum([fin.total_anticipated_cost for fin in project_financials])),
        "overall_progress" : {
            "planned" : avg([p.planned_progress for p in planning]),
            "actual" : avg([m.actual_progress for m in monthlysubmissions]),
        },
        "overall_expenditure" : {
            "perc_expenditure" : avg([
                fin.percentage_expenditure(year, month) for fin in project_financials
            ]),
            "actual_expenditure" : sum([m.actual_expenditure for m in monthlysubmissions]),

        }
    }

def district_report(request, district_id, year, month):
    district = get_object_or_404(models.District, pk=district_id)
    js = {
        "name" : district.name,
        "clients" : {
            c.name : district_client_json(district, c, year, month) for c in models.Client.objects.all()
        },
    }
    return HttpResponse(json.dumps(js), mimetype="application/json")

