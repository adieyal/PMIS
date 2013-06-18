import decimal
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
        print request.user
        print request.DATA.get('project', {})
        project_id = request.DATA.get('project', {}).get('id', '')
        project = request.DATA.get('project', {})
        print project
        instance = Project.objects.get(id=project_id)
        for item in instance._meta.fields:
            if item.rel:
                if getattr(instance, item.name).id == project.get(item.name, {}).get('id', ''):
                    print "Don't change field: %s" % item.name
                else:
                    print '----------------------'
                    print getattr(instance, item.name)
                    print project.get(item.name)
                    print "Change field: %s" % item.name
                    print '----------------------'
                    setattr(instance, '%s_id' % item.name, project.get(item.name, {}).get('id', ''))
            else:
                if getattr(instance, item.name) == project.get(item.name):
                    print "Don't change field: %s" % item.name
                else:
                    print '----------------------'
                    print getattr(instance, item.name)
                    print project.get(item.name)
                    print "Change field: %s" % item.name
                    print '----------------------'
                    setattr(instance, item.name, project.get(item.name))
        project_role = project.get('project_role', {})
        print project_role
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
        print planning
        for p in planning:
            year = dateutil.parser.parse(p.get('name', '')).year
            month = p.get('month', [])
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
                        p.save()

        with reversion.create_revision():
            instance.save()
            reversion.set_user(request.user)
            reversion.add_meta(Versioned, update_user=request.user, update_comment=project.get("update_comment", ""))

        print project_id
        print instance
        return Response({'status': status.HTTP_200_OK})


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
