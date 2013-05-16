from rest_framework import viewsets, generics
from rest_framework.response import Response
from project.apps.projects.models import Client, District, Municipality, Project
from serializers import ClientSerializer, DistrictSerializer, MunicipalitySerializer, ProgrammeSerializer, ProjectSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class MunicipalityViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            queryset = District.objects.get(id=pk).municipalities.all()
        except District.DoesNotExist:
            queryset = {}
        serializer = MunicipalitySerializer(queryset, many=True)
        return Response(serializer.data)


class ProgrammeViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            queryset = Client.objects.get(id=pk).programmes.all()
        except Client.DoesNotExist:
            queryset = {}
        serializer = ProgrammeSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            # queryset = Client.objects.get(id=pk).programmes__projects.all()
            queryset = Project.latest.filter(programme__client__id=pk)
        except Project.DoesNotExist:
            queryset = {}
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
