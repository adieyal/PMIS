from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import json
import project.apps.projects.models as models

"""
JSON views to product reports
"""

def district_client_json(district, client):
    #projects = models.Project.objects.filter(programme__client=client)
    project_financials = models.ProjectFinancial.objects.filter(
        project__programme__client=client, project__municipality__district=district
    )
    return {
        "total_budget" : float(sum([fin.total_anticipated_cost for fin in project_financials]))
    }

def district_report(request, district_id, year, month):
    district = get_object_or_404(models.District, pk=district_id)
    js = {
        "name" : district.name,
        "clients" : {
            c.name : district_client_json(district, c) for c in models.Client.objects.all()
        },
    }
    return HttpResponse(json.dumps(js), mimetype="application/json")
