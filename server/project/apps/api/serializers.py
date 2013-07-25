import datetime
from django.db.models import Q
from rest_framework import serializers
from rest_framework.relations import RelatedField, PrimaryKeyRelatedField
from project.apps.projects import models


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Client
        fields = ('id', 'name', )


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.District
        fields = ('id', 'name', )


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Role
        fields = ('id', 'name', )


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Entity
        fields = ('id', 'name', )


class MilestoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Milestone
        fields = ('id', 'name', 'phase', 'order', )


class MunicipalitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Municipality
        fields = ('id', 'name', )


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Programme
        fields = ('id', 'name', )


class ScopeCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ScopeCode
        fields = ('id', 'name', )


def project_serializer(queryset, condensed=None):
    data = []
    if condensed != 'true':
        for item in queryset:
            scope = []
            for s in item.scope_of_works.all():
                scope += [{
                    'id': getattr(s, 'id', ''),
                    'quantity': getattr(s, 'quantity', ''),
                    'description': getattr(s, 'description', ''),
                    'scope_code': {
                        'id': getattr(s.scope_code, 'id', ''),
                        'name': getattr(s.scope_code, 'name', ''),
                    }
                }]
            try:
                budget = item.budgets.get(year=datetime.datetime.now().year)
                allocated_budget = getattr(budget, 'allocated_budget', '')
            except:
                allocated_budget = ''
            try:
                project_role = item.project_roles.get(role__name=u'Consultant')
                consultant = {
                    'id': getattr(project_role.entity, 'id', ''),
                    'name': getattr(project_role.entity, 'name', ''),
                }
            except:
                consultant = {}

            try:
                project_role = item.project_roles.get(role__name=u'Contractor')
                contractor = {
                    'id': getattr(project_role.entity, 'id', ''),
                    'name': getattr(project_role.entity, 'name', ''),
                }
            except:
                contractor = {}

            data += [{
                     'id': item.id,
                     'name': item.name,
                     'project_number': item.project_number,
                     'description': item.description,
                     'programme': {
                         'id': getattr(item.programme, 'id', ''),
                         'name': getattr(item.programme, 'name', ''),
                     },
                     'client': {
                         'id': getattr(item.programme.client, 'id', ''),
                         'name': getattr(item.programme.client, 'name', ''),
                     },
                     'municipality': {
                         'id': getattr(item.municipality, 'id', ''),
                         'name': getattr(item.municipality, 'name', ''),
                     },
                     'district':{
                         'id': getattr(item.municipality.district, 'id', ''),
                         'name': getattr(item.municipality.district, 'name', ''),
                     },
                     'scope': scope,
                     'consultant': consultant,
                     'contractor': contractor,
                     'allocated_budget': allocated_budget
                     }]
    else:
        data = [{'id': obj.id, 'name': obj.name} for obj in queryset]
    return data


def project_detail_serializer(object):
    project_roles = []
    for pr in object.project_roles.all():
        project_roles += [{
            'id': pr.id,
            'role': pr.role.id,
            'role_name': pr.role.name,
            'entity': pr.entity_id,
        }]
    scope_of_works = []
    for sow in object.scope_of_works.all():
        scope_of_works += [{
            'id': sow.id,
            'quantity': sow.quantity,
            'scope_code': sow.scope_code.id
        }]
    budgets = []
    for b in object.budgets.all():
        plannings = []
        for p in object.plannings.filter(year=b.year):
            plannings += [{
                'id': p.id,
                'month_display': p.get_month_display(),
                'month': p.month,
                'year': p.year,
                'planned_expenses': p.planned_expenses,
                'planned_progress': p.planned_progress,
            }]

        budgets += [{
            'id': b.id,
            'year': b.year,
            'allocated_budget': b.allocated_budget,
            'allocated_planning_budget': b.allocated_planning_budget,
            'plannings': plannings
        }]
    project_milestones = []
    for pm in object.project_milestone.all():
        project_milestones += [{
            'id': pm.id,
            'milestone': pm.milestone.id,
            'name': pm.milestone.name,
            'phase': pm.milestone.phase,
            'order': pm.milestone.order,
            'completion_date': pm.completion_date
        }]
    try:
        total_anticipated_cost = object.project_financial.total_anticipated_cost
        id = object.project_financial.id
    except:
        total_anticipated_cost = ''
        id = ''
    data = {
        'project': {
            'id': object.id,
            'name': object.name,
            'description': object.description,
            'project_number': object.project_number,
            'programme': object.programme.id,
            'programme_name': object.programme.name,
            'municipality': object.municipality.id,
            'municipality_name': object.municipality.name,
            'district': object.municipality.district.id,
            'district_name': object.municipality.district.name
        },
        'project_roles': project_roles,
        'budgets': budgets,
        'project_financial': {
            'id': id,
            'total_anticipated_cost': total_anticipated_cost
        },
        'scope_of_works': scope_of_works,
        'project_milestones': project_milestones,
    }

    return data


def progress_serializer(project, year):
    data = []
    if year:
        plannings = project.plannings.in_financial_year(year)
        for p in plannings:
            try:
                monthly_submission = project.monthly_submissions.get(month=p.month, year=p.year)
                actual_progress = getattr(monthly_submission, 'actual_progress', '')
            except:
                actual_progress = ''

            data += [{
                'month': p.get_month_display(),
                'planned': getattr(p, 'planned_progress', ''),
                'actual': actual_progress
            }]
    else:
        plannings = project.plannings.all()
        for p in plannings:
            try:
                monthly_submission = project.monthly_submissions.get(month=p.month, year=p.year)
                actual_progress = getattr(monthly_submission, 'actual_progress', '')
            except:
                actual_progress = ''

            data += [{'year': p.year, 'month': p.get_month_display(), 'planned': getattr(p, 'planned_progress', ''),
                      'actual': actual_progress}]

    return data
