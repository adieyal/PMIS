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


class ProjectSerializer(serializers.ModelSerializer):
    municipality = PrimaryKeyRelatedField(many=True)
    project_financial = serializers.SlugRelatedField(slug_field='total_anticipated_cost')

    class Meta:
        model = Project
        fields = ('vid', 'cid', 'name', 'description', 'programme', 'municipality', 'project_financial' )