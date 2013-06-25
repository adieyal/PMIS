import dateutil.parser
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
import reversion
from project.apps.api.forms import ProjectTestForm, ProjectRoleTestForm, BudgetTestForm, PlanningTestForm, ProjectMilestoneTestForm, ScopeOfWorkTestForm, ProjectFinancialTestForm
from project.apps.projects.models import Client, District, Project, Programme, ScopeCode, Role, Entity, Milestone, ScopeOfWork, ProjectRole, ProjectMilestone, Planning, Budget, ProjectFinancial, Versioned
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


class ProjectsView(generics.ListAPIView):
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
        data_project = request.DATA.get('project')
        new_project = {
            'name': data_project.get('name', ''),
            'project_number': data_project.get('project_number', ''),
            'description': data_project.get('description', ''),
            'programme_id': data_project.get('programme', {}).get('id', ''),
            'municipality_id': data_project.get('municipality', {}).get('id', '')
        }
        if new_project['name'] == "" or new_project['programme_id'] == '' or new_project['municipality_id'] == '':
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        project = Project(name=new_project['name'], project_number=new_project['project_number'],
                          description=new_project['description'], programme_id=new_project['programme_id'],
                          municipality_id=new_project['municipality_id'])
        project.save()

        data_scope_of_work = request.DATA.get('scope_of_work', [])

        for scope in data_scope_of_work:
            scope_code_id = scope.get('scope_code', {})
            if scope_code_id != '':
                scope_code_id = scope_code_id.get('id', '')
            quantity = scope.get('quantity', None)
            if scope_code_id:
                scope_of_work = ScopeOfWork(scope_code_id=scope_code_id,  project_id=project.id)
                scope_of_work.save()
            if quantity:
                scope_of_work.quantity = quantity
                scope_of_work.save()

        data_project_role = request.DATA.get('project_role', [])
        for project_role_item in data_project_role:
            role_id = project_role_item.get('role', {}).get('id', '')
            entity_id = project_role_item.get('entity', {}).get('id', '')

            if role_id and entity_id:
                project_role = ProjectRole(project_id=project.id, entity_id=entity_id, role_id=role_id)
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
            year = dateutil.parser.parse(planning.get('name', '')).year
            allocated_budget = planning.get('allocated_budget', '')
            allocated_planning_budget = planning.get('allocated_planning_budget', '')

            budget = Budget(year=year, project_id=project.id)
            budget.save()
            if allocated_budget:
                budget.allocated_budget = allocated_budget
                budget.save()

            if allocated_planning_budget:
                budget.allocated_planning_budget = allocated_planning_budget
                budget.save()

            if year:
                for month in planning.get('month', []):
                    planned_expenses = month.get('planning', {}).get('planned_expenses', '')
                    planned_progress = month.get('planning', {}).get('planned_progress', '')
                    month_id = month.get('id', '')
                    if month_id:
                        p = Planning(month=month_id, year=year, project_id=project.id)
                        if planned_expenses:
                            p.planned_expenses = planned_expenses
                        if planned_progress:
                            p.planned_progress = planned_progress
                        p.save()

        project_financial = request.DATA.get('project_financial', {})
        total_anticipated_cost = project_financial.get('total_anticipated_cost', '')
        if total_anticipated_cost:
            pf = ProjectFinancial(total_anticipated_cost=total_anticipated_cost, project_id=project.id)
            pf.save()

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
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id, municipality__district_id=district_id).distinct()
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


class ProjectDetailView(generics.SingleObjectAPIView):
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

        project_id = request.DATA.get('project', {}).get('id', '')
        project = request.DATA.get('project', {})
        instance = Project.objects.get(id=project_id)
        project_data = {
            'id': project.get('id', ''),
            'name': project.get('name', ''),
            'programme': project.get('programme', {}).get('id', ''),
            'project_number': project.get('project_number', ''),
            'description': project.get('description', ''),
            'municipality': project.get('municipality', {}).get('id', '')

        }

        project_form = ProjectTestForm(project_data)
        if project_form.is_valid():
            project_form.save()
            instance = project_form.instance

        project_role = project.get('project_role', [])
        for pr in project_role:
            pr_id = pr.get('id', '')

            project_role_data = {
                'id': pr_id,
                'role': pr.get('role', {}).get('id', ''),
                'entity': pr.get('entity', {}).get('id', ''),
                'project': instance.id
            }

            project_role_form = ProjectRoleTestForm(project_role_data)
            if project_role_form.is_valid():
                project_role_form.save()

        planning = project.get('planning', [])
        for p in planning:
            year = dateutil.parser.parse(p.get('name', '')).year
            month = p.get('month', [])

            budget_data = {
                'id': p.get('id', ''),
                'year': dateutil.parser.parse(p.get('name', '')).year,
                'allocated_budget': p.get('allocated_budget', ''),
                'allocated_planning_budget': p.get('allocated_planning_budget', ''),
                'project': instance.id
            }

            budget_form = BudgetTestForm(budget_data)
            if budget_form.is_valid():
                budget_form.save()

            for m in month:
                planning_data = {
                    'id': m.get('id', ''),
                    'month': m.get('month_id', ''),
                    'year': year,
                    'planned_expenses': m.get('planning', {}).get('planned_expenses', ''),
                    'planned_progress': m.get('planning', {}).get('planned_progress', ''),
                    'project': instance.id
                }

                planning_form = PlanningTestForm(planning_data)
                if planning_form.is_valid():
                    planning_form.save()

        project_milestones = project.get('project_milestones', [])
        for pm in project_milestones:
            completion_date = pm.get('completion_date', '')
            project_milestone_data = {
                'id': pm.get('id', ''),
                'completion_date': dateutil.parser.parse(completion_date) if completion_date else None,
                'milestone': pm.get('milestone_id', ''),
                'project': instance.id
            }

            project_milestone_form = ProjectMilestoneTestForm(project_milestone_data)
            if project_milestone_form.is_valid():
                project_milestone_form.save()

        scope_of_work = project.get('scope_of_work')
        for sow in scope_of_work:

            scope_of_work_data = {
                'id': sow.get('id', ''),
                'quantity': sow.get('quantity', ''),
                'scope_code': sow.get('scope_code', {}).get('id', ''),
                'project': instance.id
            }

            scope_of_work_form = ScopeOfWorkTestForm(scope_of_work_data)
            if scope_of_work_form.is_valid():
                scope_of_work_form.save()

        project_financial = project.get('project_financial', {})

        project_financial_data = {
            'id': project_financial.get('id', ''),
            'total_anticipated_cost': project_financial.get('total_anticipated_cost', ''),
            'project': instance.id
        }

        project_financial_form = ProjectFinancialTestForm(project_financial_data)

        if project_financial_form.is_valid():
            project_financial_form.save()

        with reversion.create_revision():
            instance.save()
            reversion.set_user(request.user)
            reversion.add_meta(Versioned, update_user=request.user, update_comment=project.get("update_comment", ""))

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
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id, municipality__district_id=district_id).distinct()
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
            queryset = Project.objects.get_project(request.user.id)\
                .district(district_id)\
                .client(client_id)\
                .distinct()
        except Project.DoesNotExist:
            return Response(res)

        projects = [obj.get_progress(year=year) for obj in queryset if obj.get_progress(year=year)]

        length = len(projects)
        if length:
            sum_data = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), projects)
            res = {'actual_progress': sum_data['actual_progress'] / length, 'planned_progress': sum_data['planned_progress'] / length}

        return Response(res)
