import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from project.apps.projects import factories

client = Client()

class DistrictTest(TestCase):
    def setUp(self):
        self.district1 = factories.DistrictFactory.create()
        self.district2 = factories.DistrictFactory.create()
        self.municipality1 = factories.MunicipalityFactory(district=self.district1)
        self.municipality2 = factories.MunicipalityFactory(district=self.district1)
        self.municipality3 = factories.MunicipalityFactory(district=self.district2)


        self.url = "/api/reports/district/%s/%s/%s/"
        
    def test_district_validates_factory(self):
        # TODO - not sure why reverse doesn't work
        #print reverse("reports_district", kwargs={"district_id" : "1234"})

        response = client.get(self.url % (1234, 2013, 6))
        self.assertEquals(response.status_code, 404)

        response = client.get(self.url % (self.district1.id, 2013, 6))
        self.assertEquals(response.status_code, 200)

    def test_district_returns_data(self):
        response = client.get(self.url % (self.district1.id, 2013, 6))
        js = json.loads(response.content)
        self.assertEquals(js["name"], self.district1.name)

    def test_district_returns_clients(self):
        client1 = factories.ClientFactory.create()
        client2 = factories.ClientFactory.create()

        response = client.get(self.url % (self.district1.id, 2013, 6))
        js = json.loads(response.content)
        self.assertTrue("clients" in js)
        self.assertEquals(type(js["clients"]), dict)
        self.assertEquals(len(js["clients"]), 2)
        self.assertTrue(client1.name in js["clients"])
        self.assertTrue(client2.name in js["clients"])
        self.assertEquals(type(js["clients"][client1.name]), dict)
        
    def test_district_returns_total_budget_per_client(self):
        # Both in the same municipality and programme/client
        project1 = factories.ProjectFactory()
        project2 = factories.ProjectFactory(
            programme=project1.programme, municipality=project1.municipality
        )

        # Same municipality but different programme/client
        project3 = factories.ProjectFactory(municipality=project1.municipality)

        # Same programme different district - doesn't affect total
        project4 = factories.ProjectFactory(programme=project1.programme)

        fin1 = factories.ProjectFinancialFactory(project=project1, total_anticipated_cost=100)
        fin2 = factories.ProjectFinancialFactory(project=project2, total_anticipated_cost=50)
        fin3 = factories.ProjectFinancialFactory(project=project3, total_anticipated_cost=60)
        fin4 = factories.ProjectFinancialFactory(project=project4, total_anticipated_cost=200)

        client1 = project1.programme.client
        client2 = project3.programme.client

        response = client.get(self.url % (project1.municipality.district.id, 2013, 6))
        js = json.loads(response.content)

        client1 = js["clients"][client1.name]
        client2 = js["clients"][client2.name]

        self.assertTrue("total_budget" in client1)
        self.assertEquals(client1["total_budget"], 150)
        self.assertEquals(client2["total_budget"], 60)
