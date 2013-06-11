from rest_framework import serializers
from rest_framework.relations import RelatedField, PrimaryKeyRelatedField
from project.apps.projects.models import Client, District, Municipality, Programme, Project, ScopeCode, Role, Entity, Milestone


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', )


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', )


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', )


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ('id', 'name', )


class MilestoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Milestone
        fields = ('id', 'name', 'phase', 'order', )


class MunicipalitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Municipality
        fields = ('id', 'name', )


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Programme
        fields = ('id', 'name', )


class ScopeCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScopeCode
        fields = ('id', 'name', )


def project_serializer(queryset):
    data = []
    for item in queryset:
        data += [{'id': item.id, 'name': item.name, 'description': item.description, 'programme': item.programme.id,
                  'municipality': getattr(item.municipality, 'id', ''),
                  # 'total_anticipated_cost': item.project_financial.total_anticipated_cost
                 }]
    return data


def project_detail_serializer(object):
    project_role = []
    for pr in object.project_roles.all():
        project_role += [{
            'role': {
                'id': pr.role.id,
                'name': pr.role.name
            },
            'entity': pr.entity.name
        }]
    scope_of_work = []
    for sow in object.scope_of_works.all():
        scope_of_work += [{
            'quantity': sow.quantity,
            'scope_code': {
                'id': sow.scope_code.id,
                'name': sow.scope_code.name
            }
        }]
    data = {
        'project': {
            'id': object.id,
            'name': object.name,
            'description': object.description,
            'project_number': object.project_number,
            'programme': {
                'id': object.programme.id,
                'name': object.programme.name
            },
            'municipality': {
                'id': getattr(object.municipality, 'id', ''),
                'name': getattr(object.municipality, 'name', '')
            },
            'project_role': project_role,
            'scope_of_work': scope_of_work
        }
    }

    return data


def progress_serializer(project):
    data = {'id': project.id, 'planned_expenses': 0, 'planned_progress': 0, 'actual_expenditure': 0,
            'actual_progress': 0}
    for planning in project.plannings.all():
        data['planned_expenses'] += planning.planned_expenses
        data['planned_progress'] += planning.planned_expenses

    for monthly_submission in project.monthly_submissions.all():
        data['actual_expenditure'] += monthly_submission.actual_expenditure
        data['actual_progress'] += monthly_submission.actual_progress

    return data