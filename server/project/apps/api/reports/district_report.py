from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import json
import project.apps.projects.models as models
import project.apps.api.serializers as serializers

"""
JSON views to product reports
"""

def avg(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)

def district_client_json(district, client, year, month):
    financial_year = models.FinancialYearManager.financial_year(year, month)
    infinyear = lambda dt : models.FinancialYearManager.date_in_financial_year(financial_year, dt)

    projects = models.Project.objects.client(client).district(district)
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

    #print "Districts: %s" % [p.district for p in projects]
    return {
        "fullname" : client.description,
        "name" : client.name,
        "num_jobs" : 999,
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
            "planned_expenditure" : sum([p.planned_expenses for p in planning]),

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
        }
    }


def district_report_json(district_id, year, month):
    year = int(year)
    month = int(month)

    district = get_object_or_404(models.District, pk=district_id)
    best_projects = models.Project.objects.district(district).best_performing(year, month, count=3)
    worst_projects = models.Project.objects.district(district).worst_performing(year, month, count=3)
    js = {
        "name" : district.name,
        "clients" : [
            district_client_json(district, c, year, month) for c in models.Client.objects.all()
        ],
        "projects" : {
            "best_performing" : [
                serializers.condensed_project_serializer(project, year, month)
                for project in best_projects
            ],
            "worst_performing" : [
                serializers.condensed_project_serializer(project, year, month)
                for project in worst_projects
            ],
        }
    }
    return js
    
def district_report(request, district_id, year, month):
    js = district_report_json(district_id, year, month)
    return HttpResponse(json.dumps(js, cls=serializers.ModelEncoder, indent=4), mimetype="application/json")

