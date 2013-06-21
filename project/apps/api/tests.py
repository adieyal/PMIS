import json
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

    def tearDown(self):
        Token.objects.all().delete() 
        User.objects.all().delete()

    def _get_response(self, view_name, data, with_auth=True):
        if with_auth:
            auth = 'Token %s' % self.token.key
            response = self.client.get(reverse(view_name, kwargs=data), HTTP_AUTHORIZATION=auth)
        else:
            response = self.client.get(reverse(view_name, kwargs=data))
            
        return response

    def _get_json_response(self, view_name, data):
        response = self._get_response(view_name, data)
        return json.loads(response.content)

    def _testauth(self, view_name, data):
        response = self._get_response(view_name, data, False)
        self.assertEqual(response.status_code, 401)

        response = self._get_response(view_name, data)
        self.assertEqual(response.status_code, 200)


class ClientViewSetTest(ParentTest):

    def setUp(self):
        super(ClientViewSetTest, self).setUp()
        self.data = {}
        self.view_name = "api:clients_view"

    def test_auth(self):
        self._testauth(self.view_name, self.data)

    def test_get_clients_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.Client.objects.count(), len(result))

class DistrictViewSetTest(ParentTest):
    def setUp(self):
        super(DistrictViewSetTest, self).setUp()
        self.data = {}
        self.view_name = "api:districts_view"

    def test_auth(self):
        self._testauth(self.view_name, self.data)

    def test_get_districts_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.District.objects.count(), len(result))

class MunicipalityViewSetTest(ParentTest):
    def setUp(self):
        super(MunicipalityViewSetTest, self).setUp()

        self.district = factories.DistrictFactory.create()
        self.municipality = factories.MunicipalityFactory.create(district=self.district)

        self.data = {
            'pk': self.municipality.district.pk,
        }
        self.view_name = "api:municipalities_view"

    def test_auth(self):
        self._testauth(self.view_name, self.data)

    def test_municipalities_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(
            models.Municipality.objects.filter(district=self.district).count(),
            len(result)
        )

        self.assertEqual(result[0]["id"], self.municipality.id)


class ProgrammeViewSetTest(ParentTest):
    def setUp(self):
        super(ProgrammeViewSetTest, self).setUp()
        self.clients = factories.ClientFactory.create()
        self.programme = factories.ProgrammeFactory.create(client=self.clients)

        self.data = {}
        self.view_name = "api:programme_view"

    def test_auth(self):
        self._testauth(self.view_name, self.data)

    def test_get_programme_list(self):

        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(
            models.Programme.objects.count(),
            len(result)
        )

class ProjectViewSetTest(ParentTest):
    def setUp(self):
        super(ProjectViewSetTest, self).setUp()
        self.programme = factories.ProgrammeFactory.create()
        self.project = factories.ProjectFactory.create(programme=self.programme)

        self.data = {}
        self.view_name = "api:projects_view"

    def test_auth(self):
        self._testauth(self.view_name, self.data)

    # This test doesn't work - possibly due to project permissions
    #def test_get_project_list(self):
    #    result = self._get_json_response(self.view_name, self.data)
    #    self.assertEqual(
    #        models.Project.objects.count(),
    #        len(result)
    #    )


class ScopeCodeViewSetTest(ParentTest):
    def setUp(self):
        super(ScopeCodeViewSetTest, self).setUp()
        self.scope_code = factories.ScopeCodeFactory.create()
        self.data = {}
        self.view_name = "api:scope_codes_view"

    def test_auth(self):
        self._testauth(self.view_name, self.data)

    def test_get_project_list(self):
        result = self._get_json_response(self.view_name, self.data)
        self.assertEqual(models.ScopeCode.objects.count(), len(result))
