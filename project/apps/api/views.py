import dateutil.parser
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from project.apps.projects.models import Client, District, Municipality, Project, Programme, ScopeCode, Role, Entity, Milestone, ScopeOfWork, ProjectRole, ProjectMilestone, Planning
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
        data_project = request.DATA.get('project')
        new_project = {
            'name': data_project.get('name', ''),
            'project_number': data_project.get('project_number', ''),
            'description': data_project.get('description', ''),
            'programme_id': data_project.get('programme', {}).get('id', ''),
        }
        if new_project['name'] == "" or new_project['programme_id'] == '':
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        municipalities = [x['id'] for x in data_project.get('municipalities') if x['selected'] == True]
        project = Project(name=new_project['name'], project_number=new_project['project_number'],
                          description=new_project['description'], programme_id=new_project['programme_id'])
        project.save()
        for municipality in municipalities:
            project.municipality.add(municipality)
        project.save()

        data_scope_of_work = request.DATA.get('scope_of_work', [])

        for scope in data_scope_of_work:
            scope_code_id = scope.get('scope_code', {}).get('id', '')
            quantity = scope.get('quantity', '')
            if scope_code_id:
                scope_of_work = ScopeOfWork(scope_code_id=scope_code_id, quantity=quantity, project_id=project.id)
                scope_of_work.save()

        data_project_role = request.DATA.get('project_role', [])
        for project_role_item in data_project_role:
            role_id = project_role_item.get('role', {}).get('id', '')
            entity_name = project_role_item.get('entity_name', '')

            if role_id and entity_name:
                entity, create = Entity.objects.get_or_create(name=entity_name)
                project_role = ProjectRole(project_id=project.id, entity_id=entity.id, role_id=role_id)
                project_role.save()

        data_project_milestones = request.DATA.get('project_milestones', [])
        for project_milestone in data_project_milestones:
            completion_date = project_milestone.get('completion_date', '')
            milestone_id = project_milestone.get('id', '')
            if completion_date and milestone_id:
                pm = ProjectMilestone(completion_date=dateutil.parser.parse(completion_date), milestone_id=milestone_id,
                                      project_id=project.id)
                pm.save()

        data_planning = request.DATA.get('planning', [])
        for planning in data_planning:
            year = dateutil.parser.parse(planning.get('name', ''))
            print 'year: %s' % year
            if year:
                for month in planning.get('month', []):
                    planned_expenses = month.get('planning', {}).get('amount', '')
                    planned_progress = month.get('planning', {}).get('progress', '')
                    month_id = month.get('id', '')
                    print 'planned_expenses: %s' % planned_expenses
                    print 'planned_progress: %s' % planned_progress
                    print 'month_id: %s' % month_id
                    if planned_expenses and planned_progress and month_id:
                        p = Planning(month=month_id, year=year, planned_expenses=planned_expenses,
                                     planned_progress=planned_progress, project_id=project.id)
                        p.save()
        print request.DATA
        return Response({'status': status.HTTP_201_CREATED})