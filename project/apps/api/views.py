from rest_framework import viewsets, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from project.apps.projects.models import Client, District, Municipality, Project, Programme, ScopeCode, Role, Entity, Milestone
from serializers import ClientSerializer, DistrictSerializer, MunicipalitySerializer, ProgrammeSerializer, progress_serializer, project_serializer, ScopeCodeSerializer, RoleSerializer, EntitySerializer, MilestoneSerializer


class ClientViewSet(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class ProgrammeViewSet(generics.ListAPIView):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer


class ScopeCodeViewSet(generics.ListAPIView):
    queryset = ScopeCode.objects.all()
    serializer_class = ScopeCodeSerializer


class ProjectViewSet(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        data = {}
        try:
            queryset = Project.objects.get_project(request.user.id)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class RolesViewSet(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class EntitiesViewSet(generics.ListAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class MilestonesViewSet(generics.ListAPIView):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer


class MunicipalityViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            queryset = District.objects.get(id=pk).municipalities.all()
        except District.DoesNotExist:
            queryset = {}
        serializer = MunicipalitySerializer(queryset, many=True)
        return Response(serializer.data)


class ProgrammeOfClientViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        try:
            queryset = Client.objects.get(id=pk).programmes.all()
        except Client.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class ProjectOfClientViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        try:
            queryset = Project.objects.filter(programme__client__id=pk)
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class ProjectInDistrictViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        try:
            queryset = Project.objects.filter(municipality__district__id=pk).distinct()
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class ProjectInMunicipalityViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        try:
            queryset = Project.objects.filter(municipality__id=pk).distinct()
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class ProjectInProgrammeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        try:
            queryset = Project.objects.filter(programme__id=pk).distinct()
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class ProgressView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response(data)
        data = progress_serializer(project)
        return Response(data)


class ProjectCommentsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response(data)
        data = []
        for monthly_submission in project.monthly_submissions.all():
            data += [{'month': monthly_submission.month, 'year': monthly_submission.year,
                      'comment': monthly_submission.comment, 'remedial_action': monthly_submission.remedial_action}]
        return Response(data)


class CreateProject(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        print request.DATA
        print kwargs
        return Response({'status': status.HTTP_201_CREATED})