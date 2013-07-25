import json
import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from project.apps.projects import factories, models

class ParentTest(TestCase):
    def setUp(self):
        self.clients = factories.ClientFactory.create()
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.username = 'john'
        self.email = 'lennon@thebeatles.com'
        self.password = 'password'
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.user.is_active = True
        self.user.save()
        self.token, create = Token.objects.get_or_create(user=self.user)
        self.project = None
        self._data = {}
        self._view = ""

    def tearDown(self):
        pass

    def test_auth(self):
        if self.__class__ != ParentTest:
            self._testauth(self.view_name, self.data)

    @property
    def view_name(self):
        raise NotImplementedError()

    
    @property
    def data(self):
        raise NotImplementedError()

    def _set_user_perm(self):
        if self.project:
            for group_perm_obj in self.project.group_perm_objs.all():
                for group_perm in group_perm_obj.group_perm.all():
                    group_perm.user.add(self.user)
                    group_perm.save()

    def _get_response(self, view_name, data, get_data=None, with_auth=True):
        if not get_data:
            get_data = {}
        if with_auth:
            auth = 'Token %s' % self.token.key
            response = self.client.get(reverse(view_name, kwargs=data), get_data, HTTP_AUTHORIZATION=auth)
        else:
            response = self.client.get(reverse(view_name, kwargs=data))

        return response

    def _get_json_response(self, view_name, data, get_data=None):
        if not get_data:
            get_data = {}
        response = self._get_response(view_name, data, get_data)
        return json.loads(response.content)

    def _testauth(self, view_name, data):
        response = self._get_response(view_name, data, {}, False)
        self.assertEqual(response.status_code, 401)

        response = self._get_response(view_name, data)
        self.assertEqual(response.status_code, 200)


class ClientViewSetTest(ParentTest):
    def setUp(self):
        super(ClientViewSetTest, self).setUp()

    @property
    def data(self):
        return {}

    @property
    def view_name(self):
        return "api:clients_view"

    def test_get_clients_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Client.objects.count(), len(result))


class DistrictViewSetTest(ParentTest):
    def setUp(self):
        super(DistrictViewSetTest, self).setUp()

    @property
    def data(self):
        return{}

    @property
    def view_name(self):
        return "api:districts_view"

    def test_get_districts_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.District.objects.count(), len(result))


class MunicipalityViewSetTest(ParentTest):
    def setUp(self):
        super(MunicipalityViewSetTest, self).setUp()

        self.district = factories.DistrictFactory.create()
        self.municipality = factories.MunicipalityFactory.create(district=self.district)


    @property
    def data(self):
        return { 'pk': self.municipality.district.pk }

    @property
    def view_name(self):
        return "api:municipalities_view"

    def test_municipalities_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Municipality.objects.filter(district=self.district).count(), len(result))
        self.assertEqual(result[0]["id"], self.municipality.id)


class ProgrammeViewSetTest(ParentTest):
    def setUp(self):
        super(ProgrammeViewSetTest, self).setUp()
        self.clients = factories.ClientFactory.create()
        self.programme = factories.ProgrammeFactory.create(client=self.clients)

    @property
    def data(self):
        return {}

    @property
    def view_name(self):
        return "api:programme_view"

    def test_get_programme_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Programme.objects.count(), len(result))


class ProgrammeOfClientViewSetTest(ParentTest):
    def setUp(self):
        super(ProgrammeOfClientViewSetTest, self).setUp()
        self.clients = factories.ClientFactory.create()
        self.programme = factories.ProgrammeFactory.create(client=self.clients)


    @property
    def data(self):
        return { 'pk': self.clients.id }

    @property
    def view_name(self):
        return "api:programmes_of_client_view"

    def test_get_programme_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Programme.objects.filter(client=self.clients).count(), len(result))


class ProjectViewSetTest(ParentTest):
    def setUp(self):
        super(ProjectViewSetTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)
        self._set_user_perm()

    @property
    def view_name(self):
        return "api:projects_view"
    
    @property
    def data(self):
        return {}

    # This test doesn't work - possibly due to project permissions
    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(
            models.Project.objects.count(),
            len(result)
        )


class ProjectOfClientViewSetTest(ParentTest):
    def setUp(self):
        super(ProjectOfClientViewSetTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)

        self._set_user_perm()

    @property
    def view_name(self):
        return "api:project_of_client_view"

    @property
    def data(self):
        return {
            'pk': self.project.programme.client.id
        }

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Project.objects.count(), len(result))


class ProjectOfClientOfDistrictViewSetTest(ParentTest):
    def setUp(self):
        super(ProjectOfClientOfDistrictViewSetTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)
        self._set_user_perm()

    @property
    def data(self):
        return {
            'client_id': self.project.programme.client.id,
            'district_id': self.project.municipality.district.id
        }

    @property
    def view_name(self):
        return "api:project_of_client_of_district_view"

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Project.objects.count(), len(result))


class ProjectInDistrictViewSetTest(ParentTest):
    def setUp(self):
        super(ProjectInDistrictViewSetTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)
        self._set_user_perm()

    @property
    def data(self):
        return { 'pk': self.project.municipality.district.id }

    @property
    def view_name(self):
        return "api:project_in_district_view"

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Project.objects.count(), len(result))


class ProjectInMunicipalityViewSetTest(ParentTest):
    def setUp(self):
        super(ProjectInMunicipalityViewSetTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)
        self._set_user_perm()

    @property
    def data(self):
        return { 'pk': self.project.municipality.id }

    @property
    def view_name(self):
        return "api:project_in_municipality_view"

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Project.objects.count(), len(result))

class ProjectInProgrammeViewSetTest(ParentTest):
    def setUp(self):
        super(ProjectInProgrammeViewSetTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)
        self._set_user_perm()

    @property
    def data(self):
        return { 'pk': self.project.programme.id }

    @property
    def view_name(self):
        return "api:project_in_programme_view"

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Project.objects.count(), len(result))


class ProgressViewTest(ParentTest):
    def setUp(self):
        super(ProgressViewTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)
        self.planning = factories.PlanningFactory.create(project=self.project)
        self._set_user_perm()

    @property
    def data(self):
        return { 'pk': self.project.id }

    @property
    def view_name(self):
        return "api:progress_view"

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Planning.objects.all().count(), len(result))


class ScopeCodeViewSetTest(ParentTest):
    def setUp(self):
        super(ScopeCodeViewSetTest, self).setUp()
        self.scope_code = factories.ScopeCodeFactory.create()

    @property
    def view_name(self):
        return "api:scope_codes_view"

    @property
    def data(self):
        return {}

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.ScopeCode.objects.count(), len(result))


#class ProjectTopPerformingViewSetTest(ParentTest):
#    def setUp(self):
#        super(ProjectTopPerformingViewSetTest, self).setUp()
#
#        self.programme = factories.ProgrammeFactory.create()
#        self.project = factories.ProjectFactory.create(programme=self.programme)
#
#        year, month = 2013, 6
#        self.planning = factories.PlanningFactory.create(project=self.project, year=year, month=month)
#        self.monthly_submission = factories.MonthlySubmissionFactory(project=self.project, year=year, month=month)
#
#        self.get_data = {
#            'num': 5
#        }
#        self._set_user_perm()
#
#    @property
#    def view_name(self):
#        return "api:project_top_performing_view"
#
#    @property
#    def data(self):
#        return {
#            'client_id': self.programme.client.id,
#            'district_id': self.project.municipality.district.id
#        }
#
#
#    def test_get_top_performing_project_list(self):
#        result = self._get_json_response(self.view_name, self.data, self.get_data)
#        self.assertEqual(models.Project.objects.count(), len(result))


#class ProjectWorstPerformingViewSetTest(ParentTest):
#    def setUp(self):
#        super(ProjectWorstPerformingViewSetTest, self).setUp()
#        self.programme = factories.ProgrammeFactory.create()
#        self.project = factories.ProjectFactory.create(programme=self.programme)
#        year = datetime.datetime.now().year
#        year, month = 2013, 6
#
#        self.planning = factories.PlanningFactory.create(project=self.project, year=year, month=month)
#        self.monthly_submission = factories.MonthlySubmissionFactory(project=self.project, year=year, month=month)
#
#        self.get_data = {
#            'num': 5, 'year' : year, 'month' : month
#        }
#        self._set_user_perm()
#
#    @property
#    def view_name(self):
#        return "api:project_worst_performing_view"
#
#    @property
#    def data(self):
#        return {
#            'client_id': self.programme.client.id,
#            'district_id': self.project.municipality.district.id
#        }
#
#    def test_get_worst_performing_project_list(self):
#        result = self._get_json_response(self.view_name, self.data, self.get_data)
#        self.assertEqual(models.Project.objects.count(), len(result))


#class ProjectOverallProgressViewSetTest(ParentTest):
#    def setUp(self):
#        super(ProjectOverallProgressViewSetTest, self).setUp()
#        self.programme = factories.ProgrammeFactory.create()
#        self.project = factories.ProjectFactory.create(programme=self.programme)
#        year = datetime.datetime.now().year
#        if datetime.datetime.now().month == 1:
#            month = 12
#            year -= 1
#        else:
#            month = datetime.datetime.now().month - 1
#        self.planning = factories.PlanningFactory.create(project=self.project, year=year, month=month)
#        self.monthly_submission = factories.MonthlySubmissionFactory(project=self.project, year=year, month=month)
#
#        self.get_data = {
#            # 'year': year
#        }
#        self._set_user_perm()
#
#    @property
#    def view_name(self):
#        return "api:project_overall_progress_view"
#
#    @property
#    def data(self):
#        return {
#            'client_id': self.programme.client.id,
#            'district_id': self.project.municipality.district.id
#        }
#
#    def test_project_overall_progress_view(self):
#        result = self._get_json_response(self.view_name, self.data, self.get_data)
#        self.assertEqual(result, {'actual_progress': self.monthly_submission.actual_progress, 'planned_progress': self.planning.planned_progress})
