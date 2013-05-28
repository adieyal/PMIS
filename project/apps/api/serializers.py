from rest_framework import serializers
from rest_framework.relations import RelatedField, PrimaryKeyRelatedField
from project.apps.projects.models import Client, District, Municipality, Programme, Project


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', )


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', )


class MunicipalitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Municipality
        fields = ('id', 'name', )


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Programme
        fields = ('id', 'name', )


def project_serializer(queryset):
    data = []
    for item in queryset:
        data += [{'id': item.id, 'name': item.name, 'description': item.description, 'programme': item.programme.id,
                  'municipality': [municipality.id for municipality in item.municipality.all()],
                  # 'total_anticipated_cost': item.project_financial.total_anticipated_cost
                 }]
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