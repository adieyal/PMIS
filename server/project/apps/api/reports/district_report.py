from django.http import HttpResponse, Http404
from datetime import datetime
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
        "date" : datetime(year, month, 1),
        "district" : {
            "name" : district.name,
            "id" : district.id,
        },
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
    js = district_report_json2(district_id, year, month)
    return HttpResponse(json.dumps(js, cls=serializers.ModelEncoder, indent=4), mimetype="application/json")

def district_report_json2(district_id, year, month):
    return {
        "date" : datetime(int(year), int(month), 1),
        "clients": [
            {
                "total_projects": 0, 
                "overall_expenditure": {
                    "actual_expenditure": 0, 
                    "planned_expenditure": 0, 
                    "perc_expenditure": 0
                }, 
                "name": "DCSR", 
                "overall_progress": {
                    "actual": 0, 
                    "planned": 0
                }, 
                "fullname": "Department of Culture, Sport and Recreation", 
                "total_budget": 0.0, 
                "projects": {
                    "currently_in_practical_completion": 0, 
                    "between_76_and_99": 0, 
                    "currently_in_implementation": 0, 
                    "between_51_and_75": 0, 
                    "currently_in_planning": 0, 
                    "between_0_and_50": 0, 
                    "completed_in_fye": 0, 
                    "currently_in_final_completion": 0
                }, 
                "num_jobs": 999
            }, 
            {
                "total_projects": 0, 
                "overall_expenditure": {
                    "actual_expenditure": 0, 
                    "planned_expenditure": 0, 
                    "perc_expenditure": 0
                }, 
                "name": "DEDET", 
                "overall_progress": {
                    "actual": 0, 
                    "planned": 0
                }, 
                "fullname": "Department of Economic Development and Planning", 
                "total_budget": 0.0, 
                "projects": {
                    "currently_in_practical_completion": 0, 
                    "between_76_and_99": 0, 
                    "currently_in_implementation": 0, 
                    "between_51_and_75": 0, 
                    "currently_in_planning": 0, 
                    "between_0_and_50": 0, 
                    "completed_in_fye": 0, 
                    "currently_in_final_completion": 0
                }, 
                "num_jobs": 999
            }, 
            {
                "total_projects": 13, 
                "overall_expenditure": {
                    "actual_expenditure": 9167000.0, 
                    "planned_expenditure": 47132000.0, 
                    "perc_expenditure": 0.12503002830533305
                }, 
                "name": "DoE", 
                "overall_progress": {
                    "actual": 51.15384615384615, 
                    "planned": 76.46153846153847
                }, 
                "fullname": "Department of Education", 
                "total_budget": 400621000.0, 
                "projects": {
                    "currently_in_practical_completion": 0, 
                    "between_76_and_99": 4, 
                    "currently_in_implementation": 0, 
                    "between_51_and_75": 9, 
                    "currently_in_planning": 0, 
                    "between_0_and_50": 140, 
                    "completed_in_fye": 10, 
                    "currently_in_final_completion": 0
                }, 
                "num_jobs": 999
            }, 
            {
                "total_projects": 0, 
                "overall_expenditure": {
                    "actual_expenditure": 0, 
                    "planned_expenditure": 0, 
                    "perc_expenditure": 0
                }, 
                "name": "DoH", 
                "overall_progress": {
                    "actual": 0, 
                    "planned": 0
                }, 
                "fullname": "Department of Health", 
                "total_budget": 0.0, 
                "projects": {
                    "currently_in_practical_completion": 0, 
                    "between_76_and_99": 0, 
                    "currently_in_implementation": 0, 
                    "between_51_and_75": 0, 
                    "currently_in_planning": 0, 
                    "between_0_and_50": 0, 
                    "completed_in_fye": 0, 
                    "currently_in_final_completion": 0
                }, 
                "num_jobs": 999
            }, 
            {
                "total_projects": 0, 
                "overall_expenditure": {
                    "actual_expenditure": 0, 
                    "planned_expenditure": 0, 
                    "perc_expenditure": 0
                }, 
                "name": "DSD", 
                "overall_progress": {
                    "actual": 0, 
                    "planned": 0
                }, 
                "fullname": "Department of Social Development", 
                "total_budget": 0.0, 
                "projects": {
                    "currently_in_practical_completion": 0, 
                    "between_76_and_99": 0, 
                    "currently_in_implementation": 0, 
                    "between_51_and_75": 0, 
                    "currently_in_planning": 0, 
                    "between_0_and_50": 0, 
                    "completed_in_fye": 0, 
                    "currently_in_final_completion": 0
                }, 
                "num_jobs": 999
            }, 
            {
                "total_projects": 0, 
                "overall_expenditure": {
                    "actual_expenditure": 0, 
                    "planned_expenditure": 0, 
                    "perc_expenditure": 0
                }, 
                "name": "DSSL", 
                "overall_progress": {
                    "actual": 0, 
                    "planned": 0
                }, 
                "fullname": "Department of Safety, Security and Liaison", 
                "total_budget": 0.0, 
                "projects": {
                    "currently_in_practical_completion": 0, 
                    "between_76_and_99": 0, 
                    "currently_in_implementation": 0, 
                    "between_51_and_75": 0, 
                    "currently_in_planning": 0, 
                    "between_0_and_50": 0, 
                    "completed_in_fye": 0, 
                    "currently_in_final_completion": 0
                }, 
                "num_jobs": 999
            }
        ], 
        "district" : {
            "name": "Gert Sibande", 
            "id" : 2
        },
        "projects": {
            "best_performing": [
                {
                    "client": "DoE", 
                    "jobs": 434343, 
                    "name": "Harmony Park C School", 
                    "district": {
                        "id": 2, 
                        "name": "Gert Sibande"
                    }, 
                    "expenditure": {
                        "actual": 599000.0, 
                        "ratio": 0.2396, 
                        "planned": 0.0
                    }, 
                    "progress": {
                        "actual": 94.0, 
                        "planned": 80.0
                    }, 
                    "municipality": {
                        "id": 5, 
                        "name": "Mkhondo"
                    }, 
                    "budget": 2500000.0
                }, 
                {
                    "client": "DoE", 
                    "jobs": 434343, 
                    "name": "Imizamoyethu Primary School", 
                    "district": {
                        "id": 2, 
                        "name": "Gert Sibande"
                    }, 
                    "expenditure": {
                        "actual": 107000.0, 
                        "ratio": 0.042868589743589744, 
                        "planned": 0.0
                    }, 
                    "progress": {
                        "actual": 92.0, 
                        "planned": 90.0
                    }, 
                    "municipality": {
                        "id": 5, 
                        "name": "Mkhondo"
                    }, 
                    "budget": 2496000.0
                }, 
                {
                    "client": "DoE", 
                    "jobs": 434343, 
                    "name": "Vulingcondo Primary", 
                    "district": {
                        "id": 2, 
                        "name": "Gert Sibande"
                    }, 
                    "expenditure": {
                        "actual": 0.0, 
                        "ratio": 0.0, 
                        "planned": 0.0
                    }, 
                    "progress": {
                        "actual": 99.0, 
                        "planned": 99.0
                    }, 
                    "municipality": {
                        "id": 3, 
                        "name": "Albert Luthuli"
                    }, 
                    "budget": 1428000.0
                }
            ], 
            "worst_performing": [
                {
                    "client": "DoE", 
                    "jobs": 434343, 
                    "name": "Myflower Secondary", 
                    "district": {
                        "id": 2, 
                        "name": "Gert Sibande"
                    }, 
                    "expenditure": {
                        "actual": 0.0, 
                        "ratio": 0.0, 
                        "planned": 0.0
                    }, 
                    "progress": {
                        "actual": 0.0, 
                        "planned": 60.0
                    }, 
                    "municipality": {
                        "id": 3, 
                        "name": "Albert Luthuli"
                    }, 
                    "budget": 20608000.0
                }, 
                {
                    "client": "DoE", 
                    "jobs": 434343, 
                    "name": "Methula Secondary", 
                    "district": {
                        "id": 2, 
                        "name": "Gert Sibande"
                    }, 
                    "expenditure": {
                        "actual": 0.0, 
                        "ratio": 0.0, 
                        "planned": 0.0
                    }, 
                    "progress": {
                        "actual": 0.0, 
                        "planned": 60.0
                    }, 
                    "municipality": {
                        "id": 3, 
                        "name": "Albert Luthuli"
                    }, 
                    "budget": 20608000.0
                }, 
                {
                    "client": "DoE", 
                    "jobs": 434343, 
                    "name": "Ikhethelo Secondary School", 
                    "district": {
                        "id": 2, 
                        "name": "Gert Sibande"
                    }, 
                    "expenditure": {
                        "actual": 0.0, 
                        "ratio": 0.0, 
                        "planned": 0.0
                    }, 
                    "progress": {
                        "actual": 0.0, 
                        "planned": 60.0
                    }, 
                    "municipality": {
                        "id": 9, 
                        "name": "Govan Mbeki"
                    }, 
                    "budget": 20608000.0
                }
            ]
        }
    }
    return  s
