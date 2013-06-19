from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from project.apps.projects import factories


class ClientViewSetTest(TestCase):
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
        print self.token

    def test_get_clients_list(self):
        data = {
        }
        response = self.client.get(reverse('api:clients_view', kwargs=data), )
        self.assertEqual(response.status_code, 401)
        auth = 'Token %s' % self.token.key
        print auth
        response = self.client.get(reverse('api:clients_view', kwargs=data), HTTP_AUTHORIZATION=auth)
        print response
        self.assertEqual(response.status_code, 200)


class DistrictViewSetTest(TestCase):
    def setUp(self):
        self.district = factories.DistrictFactory.create()
        self.csrf_client = Client(enforce_csrf_checks=True)
        # self.username = 'john1'
        # self.email = 'lennon1@thebeatles.com'
        # self.password = 'password'
        # self.user = User.objects.create_user(self.username, self.email, self.password)
        # self.user.is_active = True
        # self.user.save()
        # self.token, create = Token.objects.get_or_create(user=self.user)

    def test_get_districts_list(self):
        data = {
        }
        response = self.client.get(reverse('api:districts_view', kwargs=data), )
        self.assertEqual(response.status_code, 401)
        # auth = 'Token %s' % self.token.key
        # response = self.client.get(reverse('api:clients_view', kwargs=data), HTTP_AUTHORIZATION=auth)
        # self.assertEqual(response.status_code, 200)


class MunicipalityViewSetTest(TestCase):
    def setUp(self):
        self.district = factories.DistrictFactory.create(id=1)
        self.municipality = factories.MunicipalityFactory.create(district=self.district)

    def test_get_municipalities_list(self):

        data = {
            'pk': self.municipality.district.pk,
        }
        response = self.client.get(reverse('api:municipalities_view', kwargs=data), )
        self.assertEqual(response.status_code, 401)

        #
        # response = self.client.post(reverse('api:following', kwargs=data), **self.auth)
        # self.assertEqual(response.status_code, 204)


class ProgrammeViewSetTest(TestCase):
    def setUp(self):
        self.clients = factories.ClientFactory.create(id=1)
        self.programme = factories.ProgrammeFactory.create(client=self.clients)
        # self.csrf_client = Client(enforce_csrf_checks=True)
        # self.username = 'john1'
        # self.email = 'lennon1@thebeatles.com'
        # self.password = 'password'
        # self.user = User.objects.create_user(self.username, self.email, self.password)
        # self.user.is_active = True
        # self.user.save()
        # self.token, create = Token.objects.get_or_create(user=self.user)

    def test_get_programme_list(self):

        data = {}
        # auth = 'Token %s' % self.token.key
        # print auth
        response = self.client.get(reverse('api:programme_view', kwargs=data), )
        self.assertEqual(response.status_code, 401)

        # response = self.client.post(reverse('api:programme_view', kwargs=data), HTTP_AUTHORIZATION=auth)
        # print response
        # self.assertEqual(response.status_code, 204)


class ProjectViewSetTest(TestCase):
    def setUp(self):
        self.programme = factories.ProgrammeFactory.create(id=1)
        self.project = factories.ProjectFactory.create(programme=self.programme)

    def test_get_project_list(self):
        data = {}
        response = self.client.get(reverse('api:projects_view', kwargs=data), )
        self.assertEqual(response.status_code, 401)


class ScopeCodeViewSetTest(TestCase):
    def setUp(self):
        self.scope_code = factories.ScopeCodeFactory.create()

    def test_get_project_list(self):
        data = {}
        response = self.client.get(reverse('api:scope_codes_view', kwargs=data), )
        self.assertEqual(response.status_code, 401)