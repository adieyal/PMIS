import decimal
import datetime
import dateutil.parser
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import reversion
from project.apps.projects.models import Client, District, Municipality, Project, Programme, ScopeCode, Role, Entity, Milestone, ScopeOfWork, ProjectRole, ProjectMilestone, Planning, Budget, ProjectFinancial, Versioned
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
        try:
            queryset = Project.objects.get_project(request.user.id)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
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
            queryset = Project.objects.get_project(request.user.id).filter(programme__client__id=pk)
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class ProjectOfClientOfDistrictViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        district_id = kwargs.get('district_id')
        data = {}
        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id, municipality__district_id=district_id).distinct()
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
            queryset = Project.objects.get_project(request.user.id).filter(municipality__district__id=pk).distinct()
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
            queryset = Project.objects.get_project(request.user.id).filter(municipality__id=pk).distinct()
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
            queryset = Project.objects.get_project(request.user.id).filter(programme__id=pk).distinct()
            if phase:
                queryset = queryset.filter(project_milestone__milestone__phase=phase)
            if milestone:
                queryset = queryset.filter(project_milestone__milestone__name=milestone)
        except Project.DoesNotExist:
            return Response(data)
        data = project_serializer(queryset)
        return Response(data)


class ProjectDetailView(generics.SingleObjectAPIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        data = {}
        try:
            object = Project.objects.get_project(request.user.id).get(id=pk)
        except Project.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        data = project_detail_serializer(object)
        return Response(data)

    def put(self, request, *args, **kwargs):
        project_id = request.DATA.get('project', {}).get('id', '')
        project = request.DATA.get('project', {})
        instance = Project.objects.get(id=project_id)
        for item in instance._meta.fields:
            if item.rel:
                if getattr(instance, item.name).id != project.get(item.name, {}).get('id', ''):
                    setattr(instance, '%s_id' % item.name, project.get(item.name, {}).get('id', ''))
            else:
                if getattr(instance, item.name) != project.get(item.name):
                    setattr(instance, item.name, project.get(item.name))
        project_role = project.get('project_role', {})
        for pr in project_role:
            pr_id = pr.get('id', '')
            role_id = pr.get('role', {}).get('id', '')
            entity_id = pr.get('entity', {}).get('id', '')
            try:
                if pr_id:
                    project_role_obj = ProjectRole.objects.get(id=pr_id)
                    if project_role_obj.role_id != role_id:
                        project_role_obj.role_id = role_id
                        project_role_obj.save()
                    if project_role_obj.entity_id != entity_id:
                        project_role_obj.entity_id = entity_id
                        project_role_obj.save()
                else:
                    project_role_obj = ProjectRole(role_id=role_id, entity_id=entity_id, project_id=instance.id)
                    project_role_obj.save()
            except ProjectRole.DoesNotExist:
                pass
        planning = project.get('planning', [])
        for p in planning:
            year = dateutil.parser.parse(p.get('name', '')).year
            month = p.get('month', [])
            allocated_budget = p.get('allocated_budget', '')
            allocated_planning_budget = p.get('allocated_planning_budget', '')
            p_id = p.get('id', '')
            if year:
                if p_id:
                    p_obj = Budget.objects.get(id=p_id)
                    if p_obj.allocated_budget != allocated_budget:
                        p_obj.allocated_budget = allocated_budget
                        p_obj.save()
                    if p_obj.allocated_planning_budget != allocated_planning_budget:
                        p_obj.allocated_planning_budget = allocated_planning_budget
                        p_obj.save()
                else:
                    p_obj = Budget(year=year, project_id=instance.id)
                    if allocated_budget:
                        p_obj.allocated_budget = allocated_budget
                    if allocated_planning_budget:
                        p_obj.allocated_planning_budget = allocated_planning_budget
                    p_obj.save()

            for m in month:
                planning_id = m.get('id', '')
                planned_expenses = m.get('planning', {}).get('planned_expenses', '')
                planned_progress = m.get('planning', {}).get('planned_progress', '')
                month_id = m.get('month_id', '')
                if planning_id:
                    planning_obj = Planning.objects.get(id=planning_id)
                    if planning_obj.planned_expenses != planned_expenses:
                        planning_obj.planned_expenses = planned_expenses
                        planning_obj.save()
                    if planning_obj.planned_progress != planned_progress:
                        planning_obj.planned_progress = planned_progress
                        planning_obj.save()
                else:
                    if year and month_id:
                        planning_obj = Planning(month=month_id, year=year, project_id=instance.id)
                        if planned_expenses:
                            planning_obj.planned_expenses = planned_expenses
                        if planned_progress:
                            planning_obj.planned_progress = planned_progress
                        planning_obj.save()

        project_milestones = project.get('project_milestones', [])
        for pm in project_milestones:
            pm_id = pm.get('id', '')
            completion_date = pm.get('completion_date', '')
            milestone_id = pm.get('milestone_id', '')
            if pm_id:
                pm_obj = ProjectMilestone.objects.get(id=pm_id)
                if completion_date and pm_obj.completion_date != dateutil.parser.parse(completion_date):
                    pm_obj.completion_date = dateutil.parser.parse(completion_date)
                    pm_obj.save()
            else:
                pm_obj = ProjectMilestone(milestone_id=milestone_id, project_id=instance.id)
                if completion_date:
                    pm_obj.completion_date = dateutil.parser.parse(completion_date)
                else:
                    pm_obj.completion_date = None
                pm_obj.save()
        scope_of_work = project.get('scope_of_work')
        for sow in scope_of_work:
            sow_id = sow.get('id', '')
            quantity = sow.get('quantity', '')
            scope_code_id = sow.get('scope_code', {}).get('id', '')
            if sow_id:
                sow_obj = ScopeOfWork.objects.get(id=sow_id)
                if sow_obj.quantity != quantity:
                    sow_obj.quantity = quantity
                    sow_obj.save()
                if scope_code_id and sow_obj.scope_code_id != scope_code_id:
                    sow_obj.scope_code_id = scope_code_id
                    sow_obj.save()
            else:
                if scope_code_id:
                    sow_obj = ScopeOfWork(project_id=instance.id, scope_code_id=scope_code_id)
                    if quantity:
                        sow_obj.quantity = quantity
                    sow_obj.save()
        project_financial = project.get('project_financial', {})
        project_financial_id = project_financial.get('id', '')
        project_financial_total_anticipated_cost = project_financial.get('total_anticipated_cost', '')
        if project_financial_id:
            pf_obj = ProjectFinancial.objects.get(id=project_financial_id)
            if pf_obj.total_anticipated_cost != project_financial_total_anticipated_cost:
                pf_obj.total_anticipated_cost = project_financial_total_anticipated_cost
                pf_obj.save()
        else:
            pf_obj = ProjectFinancial(project_id=instance.id)
            if project_financial_total_anticipated_cost:
                pf_obj.total_anticipated_cost = project_financial_total_anticipated_cost
            pf_obj.save()

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
            data += [{'month': monthly_submission.month, 'year': monthly_submission.year,
                      'comment': monthly_submission.comment, 'remedial_action': monthly_submission.remedial_action}]
        return Response(data)


class ProjectTopPerformingViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        district_id = kwargs.get('district_id')
        num = request.GET.get('num', None)
        data = {}
        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id, municipality__district_id=district_id).distinct()
        except Project.DoesNotExist:
            return Response(data)

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month - 1
        # print queryset.values_list('id', )
        projects = []
        for x in queryset:
            try:
                print x
                print x.plannings.values_list('id', 'month', 'year')
                print x.monthly_submissions.values_list('id', 'month', 'year')
                y = x.plannings.get(year=year, month=month)
                print getattr(y, 'planned_progress', '')
                print '--------monthly_submissions-----------'
                z = x.monthly_submissions.get(year=year, month=month)
                print getattr(z, 'actual_progress', '')
            except:
                print 'except'



        data = project_serializer(queryset)
        return Response(data)


class ProjectWorstPerformingViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        district_id = kwargs.get('district_id')
        num = request.GET.get('num', None)
        data = {}
        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id, municipality__district_id=district_id).distinct()
        except Project.DoesNotExist:
            return Response(data)

        data = project_serializer(queryset)
        return Response(data)


class ProjectOverallProgressViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        district_id = kwargs.get('district_id')
        year = request.GET.get('year', None)
        data = {}
        try:
            queryset = Project.objects.get_project(request.user.id).filter(programme__client_id=client_id, municipality__district_id=district_id).distinct()
        except Project.DoesNotExist:
            return Response(data)

        data = project_serializer(queryset)
        return Response(data)