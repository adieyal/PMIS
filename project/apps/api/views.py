import copy
import dateutil.parser
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
import reversion
from project.apps.api.forms import ProjectTestForm, ProjectRoleTestForm, BudgetTestForm, PlanningTestForm, ProjectMilestoneTestForm, ScopeOfWorkTestForm, ProjectFinancialTestForm
from project.apps.projects.models import Client, District, Project, Programme, ScopeCode, Role, Entity, Milestone, Versioned
from serializers import ClientSerializer, DistrictSerializer, MunicipalitySerializer, ProgrammeSerializer, progress_serializer, project_serializer, ScopeCodeSerializer, RoleSerializer, EntitySerializer, MilestoneSerializer, project_detail_serializer


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


class ProcessDataProjectMixin(object):
    def process_data(self, request):
        project_data = request.DATA.get('project', {})
        project_form = ProjectTestForm(project_data)
        if project_form.is_valid():
            project_form.save()
            instance = project_form.instance
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        project_roles = request.DATA.get('project_roles', [])

        for pr in project_roles:
            project_role_data = pr.update({u'project': instance.id}) or pr
            project_role_form = ProjectRoleTestForm(project_role_data)
            if project_role_form.is_valid():
                project_role_form.save()

        budgets = request.DATA.get('budgets', [])
        for p in budgets:
            budget_data = p.update({'project': instance.id}) or p

            budget_form = BudgetTestForm(budget_data)
            if budget_form.is_valid():
                budget_form.save()

            plannings = p.get('plannings', [])
            for planning in plannings:
                planning_data = planning.update({'project': instance.id}) or planning
                planning_form = PlanningTestForm(planning_data)
                if planning_form.is_valid():
                    planning_form.save()

        project_milestones = request.DATA.get('project_milestones', [])
        for pm in project_milestones:
            project_milestone_data = pm.update({'project': instance.id}) or pm

            project_milestone_form = ProjectMilestoneTestForm(project_milestone_data)
            if project_milestone_form.is_valid():
                project_milestone_form.save()

        scope_of_works = request.DATA.get('scope_of_works', [])
        for sow in scope_of_works:
            scope_of_work_data = sow.update({'project': instance.id}) or sow
            scope_of_work_form = ScopeOfWorkTestForm(scope_of_work_data)
            if scope_of_work_form.is_valid():
                scope_of_work_form.save()

        project_financial = request.DATA.get('project_financial', {})
        project_financial_data = project_financial.update({u'project': instance.id}) or project_financial

        project_financial_form = ProjectFinancialTestForm(project_financial_data)

        if project_financial_form.is_valid():
            project_financial_form.save()

        with reversion.create_revision():
            instance.save()
            reversion.set_user(request.user)
            reversion.add_meta(Versioned, update_user=request.user, update_comment=request.DATA.get("update_comment", 'Initialization of the project.'))


class ProjectsView(ProcessDataProjectMixin, generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        data = {}
        condensed = request.GET.get('condensed', None)

        try:
            queryset = Project.objects.get_project(request.user.id)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset, condensed)
        return Response(data)

    def post(self, request, *args, **kwargs):

        self.process_data(request)

        return Response({'status': status.HTTP_201_CREATED})


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


class ProgrammeOfClientViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            queryset = Client.objects.get(id=pk).programmes.all()
        except District.DoesNotExist:
            queryset = {}
        serializer = ProgrammeSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectOfClientViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        condensed = request.GET.get('condensed', None)

        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__client__id=pk)
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset, condensed)
        return Response(data)


class ProjectOfClientOfDistrictViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        district_id = kwargs.get('district_id')
        condensed = request.GET.get('condensed', None)

        data = {}
        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id,
                                                                           municipality__district_id=district_id).distinct()
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset, condensed)
        return Response(data)


class ProjectInDistrictViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        condensed = request.GET.get('condensed', None)

        try:
            queryset = Project.objects.get_project(request.user.id).filter(municipality__district__id=pk).distinct()
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset, condensed)
        return Response(data)


class ProjectInMunicipalityViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        condensed = request.GET.get('condensed', None)

        try:
            queryset = Project.objects.get_project(request.user.id).filter(municipality__id=pk).distinct()
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset, condensed)
        return Response(data)


class ProjectInProgrammeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        phase = request.GET.get('phase', None)
        milestone = request.GET.get('milestone', None)
        condensed = request.GET.get('condensed', None)

        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__id=pk).distinct()
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset, condensed)
        return Response(data)


class ProjectDetailView(ProcessDataProjectMixin, generics.SingleObjectAPIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        data = {}

        try:
            obj = Project.objects.get_project(request.user.id).get(id=pk)
        except Project.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        data = project_detail_serializer(obj)
        return Response(data)

    def put(self, request, *args, **kwargs):

        self.process_data(request)

        return Response({'status': status.HTTP_200_OK})


class ProgressView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        data = {}
        year = request.GET.get('year', None)
        pk = kwargs.get('pk')
        try:
            project = Project.objects.get_project(request.user.id).get(id=pk)
        except Project.DoesNotExist:
            return Response(data)
        data = progress_serializer(project, year)
        return Response(data)


class ProjectCommentsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        data = {}
        try:
            project = Project.objects.get_project(request.user.id).get(id=pk)
        except Project.DoesNotExist:
            return Response(data)
        data = []
        for monthly_submission in project.monthly_submissions.all():
            data += [{
                         'month': monthly_submission.month,
                         'year': monthly_submission.year,
                         'comment': monthly_submission.comment,
                         'remedial_action': monthly_submission.remedial_action
                     }]
        return Response(data)


class ProjectTopPerformingViewSet(generics.ListAPIView):
    order = 1

    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        district_id = kwargs.get('district_id')
        condensed = request.GET.get('condensed', None)
        num = request.GET.get('num', None)
        data = {}
        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id,
                                                                           municipality__district_id=district_id).distinct()
        except Project.DoesNotExist:
            return Response(data)

        projects = [{'value': obj.get_performing(), 'id': obj.id} for obj in queryset if obj.get_performing()]

        projects = sorted(projects, key=lambda k: self.order * k['value'])

        try:
            if int(num) > 0:
                projects = projects[0:int(num)]
        except:
            pass

        project_ids = [item['id'] for item in projects]

        queryset = Project.objects.get_project(request.user.id).filter(id__in=project_ids).distinct()

        data = project_serializer(queryset, condensed)
        return Response(data)


class ProjectWorstPerformingViewSet(ProjectTopPerformingViewSet):
    order = -1


class ProjectOverallProgressViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        district_id = kwargs.get('district_id')
        year = request.GET.get('year', None)
        res = {}
        try:
            queryset = Project.objects.get_project(request.user.id) \
                .district(district_id) \
                .client(client_id) \
                .distinct()
        except Project.DoesNotExist:
            return Response(res)

        projects = [obj.get_progress(year=year) for obj in queryset if obj.get_progress(year=year)]

        length = len(projects)
        if length:
            sum_data = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), projects)
            res = {'actual_progress': sum_data['actual_progress'] / length,
                   'planned_progress': sum_data['planned_progress'] / length}

        return Response(res)
