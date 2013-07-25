import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from project.apps.projects import factories

client = Client()

class DistrictTest(TestCase):
    def setUp(self):

        # TODO - not sure why reverse doesn't work
        #self.url = reverse("reports_district", kwargs={"district_id" : "1234"})

        self.url = "/api/reports/district/%s/%s/%s/"

        # Both in the same municipality and programme/client
        self.project1 = factories.ProjectFactory()
        self.project2 = factories.ProjectFactory(
            programme=self.project1.programme, municipality=self.project1.municipality
        )

        # Same municipality but different programme/client
        self.project3 = factories.ProjectFactory(municipality=self.project1.municipality)

        # Same programme different district - doesn't affect total
        self.project4 = factories.ProjectFactory(programme=self.project1.programme)
        self.client1 = self.project1.programme.client
        self.client2 = self.project3.programme.client

        factories.ProjectFinancialFactory(project=self.project1, total_anticipated_cost=100)
        factories.ProjectFinancialFactory(project=self.project2, total_anticipated_cost=50)
        factories.ProjectFinancialFactory(project=self.project3, total_anticipated_cost=60)
        factories.ProjectFinancialFactory(project=self.project4, total_anticipated_cost=200)

        factories.PlanningFactory(project=self.project1, year=2013, month=6, planned_progress=100)
        factories.PlanningFactory(project=self.project2, year=2013, month=6, planned_progress=50)
        factories.PlanningFactory(project=self.project3, year=2013, month=6, planned_progress=25)


        factories.MonthlySubmissionFactory(
            project=self.project1, year=2013, month=6, actual_expenditure=100, actual_progress=80
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project2, year=2013, month=6, actual_expenditure=10, actual_progress=40
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project3, year=2013, month=6, actual_expenditure=300, actual_progress=100
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project4, year=2013, month=6, actual_expenditure=400, actual_progress=20
        ) 

        self.response = client.get(self.url % (self.project1.municipality.district.id, 2013, 6))
        self.js = json.loads(self.response.content)


    def test_district_validates_factory(self):
        response = client.get(self.url % (1234, 2013, 6))
        self.assertEquals(response.status_code, 404)

        response = client.get(self.url % (self.project1.municipality.district.id, 2013, 6))
        self.assertEquals(self.response.status_code, 200)

    def test_district_returns_data(self):
        self.assertEquals(self.js["name"], self.project1.municipality.district.name)

    def test_district_returns_clients(self):
        
        district = self.project1.municipality.district
        client1 = self.project1.programme.client
        client3 = self.project3.programme.client
        js = self.js

        self.assertTrue("clients" in js)
        self.assertEquals(type(js["clients"]), dict)

        self.assertEquals(len(js["clients"]), 2)
        self.assertTrue(client1.name in js["clients"])
        self.assertTrue(client3.name in js["clients"])
        self.assertEquals(type(js["clients"][client1.name]), dict)
        
    def test_district_returns_total_budget_per_client(self):

        client1 = self.project1.programme.client
        client2 = self.project3.programme.client
        js = self.js

        client1 = js["clients"][client1.name]
        client2 = js["clients"][client2.name]

        self.assertTrue("total_budget" in client1)
        self.assertEquals(client1["total_budget"], 150)
        self.assertEquals(client2["total_budget"], 60)

    def test_overall_planned_progress(self):
        js = self.js

        client1 = js["clients"][self.client1.name]
        self.assertTrue("overall_progress" in client1)
        self.assertTrue("planned" in client1["overall_progress"])
        self.assertEquals(client1["overall_progress"]["planned"], 75)

        client2 = js["clients"][self.client2.name]
        self.assertEquals(client2["overall_progress"]["planned"], 25)

    def test_overall_actual_progress(self):
        js = self.js

        client1 = js["clients"][self.client1.name]
        self.assertTrue("actual" in client1["overall_progress"])
        self.assertEquals(client1["overall_progress"]["actual"], 60)

        client2 = js["clients"][self.client2.name]
        self.assertEquals(client2["overall_progress"]["actual"], 100)

    def test_implementation_expenditure(self):
        
        client1 = self.js["clients"][self.client1.name]
        self.assertTrue("overall_expenditure" in client1)
        self.assertTrue("perc_expenditure" in client1["overall_expenditure"])
        self.assertEquals(client1["overall_expenditure"]["perc_expenditure"], 60)

        client2 = self.js["clients"][self.client2.name]
        self.assertEquals(client2["overall_expenditure"]["perc_expenditure"], 500)

    def test_actual_expenditure(self):
        js = self.js 
        client1 = self.js["clients"][self.client1.name]
        self.assertTrue("actual_expenditure" in client1["overall_expenditure"])
        self.assertEquals(client1["overall_expenditure"]["actual_expenditure"], 110)