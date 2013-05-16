from rest_framework import serializers
from project.apps.projects.models import Client, District, Municipality, Programme


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