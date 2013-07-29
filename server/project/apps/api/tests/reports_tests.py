import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from project.apps.projects import factories, models
import project.apps.api.serializers as serializers
from datetime import datetime

client = Client()

class DistrictTest(TestCase):
    def setUp(self):

        # TODO - not sure why reverse doesn't work
        #self.url = reverse("reports_district", kwargs={"district_id" : "1234"})

        self.url = "/api/reports/district/%s/%s/%s/"
        self.year, self.month = 2013, 6

        # Both in the same municipality and programme/client
        self.project1 = factories.ProjectFactory(current_step=models.Milestone.tendering_milestone())
        self.project2 = factories.ProjectFactory(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_completion()
        )

        # Same municipality but different programme/client
        self.project3 = factories.ProjectFactory(municipality=self.project1.municipality, current_step=models.Milestone.practical_completion())

        # Same programme different district - doesn't affect total
        self.project4 = factories.ProjectFactory(programme=self.project1.programme)

        self.client1 = self.project1.programme.client
        self.client2 = self.project3.programme.client

        factories.ProjectFinancialFactory(project=self.project1, total_anticipated_cost=100)
        factories.ProjectFinancialFactory(project=self.project2, total_anticipated_cost=50)
        factories.ProjectFinancialFactory(project=self.project3, total_anticipated_cost=60)
        factories.ProjectFinancialFactory(project=self.project4, total_anticipated_cost=200)

        factories.PlanningFactory(project=self.project1, year=self.year, month=self.month, planned_progress=200, planned_expenses="50")
        factories.PlanningFactory(project=self.project2, year=self.year, month=self.month, planned_progress=50, planned_expenses="70")
        factories.PlanningFactory(project=self.project3, year=self.year, month=self.month, planned_progress=25)

        factories.MonthlySubmissionFactory(
            project=self.project1, year=self.year, month=self.month, actual_expenditure=100, actual_progress=80
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project2, year=self.year, month=self.month, actual_expenditure=10, actual_progress=40
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project3, year=self.year, month=self.month, actual_expenditure=300, actual_progress=100
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project4, year=self.year, month=self.month, actual_expenditure=400, actual_progress=20
        ) 

        self.dt = datetime(year=2013, month=6, day=1) 
        self.dt2 = datetime(year=2014, month=6, day=1) 
        factories.ProjectMilestoneFactory(project=self.project1, milestone=models.Milestone.practical_completion(), completion_date=self.dt)
        factories.ProjectMilestoneFactory(project=self.project2, milestone=models.Milestone.practical_completion(), completion_date=self.dt2)
        factories.ProjectMilestoneFactory(project=self.project3, milestone=models.Milestone.practical_completion(), completion_date=self.dt2)
        factories.ProjectMilestoneFactory(project=self.project4, milestone=models.Milestone.practical_completion(), completion_date=self.dt)


        self.response = client.get(self.url % (self.project1.municipality.district.id, self.year, self.month))
        self.js = json.loads(self.response.content)
        self.client1js = self.js["clients"][0]
        self.client2js = self.js["clients"][1]


    def test_district_validates_factory(self):
        response = client.get(self.url % (1234, self.year, self.month))
        self.assertEqual(response.status_code, 404)

        response = client.get(self.url % (self.project1.municipality.district.id, self.year, self.month))
        self.assertEqual(self.response.status_code, 200)

    def test_district_returns_data(self):
        self.assertEqual(self.js["name"], self.project1.municipality.district.name)

    def test_district_returns_clients(self):
        
        district = self.project1.municipality.district
        client1 = self.project1.programme.client
        client3 = self.project3.programme.client
        js = self.js

        self.assertTrue("clients" in js)
        self.assertEqual(type(js["clients"]), list)

        self.assertEqual(len(js["clients"]), 2)
        self.assertEqual(type(self.client1js), dict)

        self.assertEqual(self.client1js["fullname"], client1.description)
        
    def test_district_returns_total_budget_per_client(self):

        self.assertTrue("total_budget" in self.client1js)
        self.assertEqual(self.client1js["total_budget"], 150)
        self.assertEqual(self.client2js["total_budget"], 60)

    def test_overall_planned_progress(self):
        js = self.js

        self.assertTrue("overall_progress" in self.client1js)
        self.assertTrue("planned" in self.client1js["overall_progress"])
        self.assertEqual(self.client1js["overall_progress"]["planned"], 125)

        self.assertEqual(self.client2js["overall_progress"]["planned"], 25)

    def test_overall_actual_progress(self):
        js = self.js

        self.assertTrue("actual" in self.client1js["overall_progress"])
        self.assertEqual(self.client1js["overall_progress"]["actual"], 60)

        self.assertEqual(self.client2js["overall_progress"]["actual"], 100)

    def test_implementation_expenditure(self):
        
        self.assertTrue("overall_expenditure" in self.client1js)
        self.assertTrue("perc_expenditure" in self.client1js["overall_expenditure"])
        self.assertEqual(self.client1js["overall_expenditure"]["perc_expenditure"], 0.60)

        self.assertEqual(self.client2js["overall_expenditure"]["perc_expenditure"], 5)

    def test_actual_expenditure(self):
        self.assertTrue("actual_expenditure" in self.client1js["overall_expenditure"])
        self.assertEqual(self.client1js["overall_expenditure"]["actual_expenditure"], 110)

    def test_planned_expenditure(self):
        self.assertTrue("planned_expenditure" in self.client1js["overall_expenditure"])
        self.assertEqual(self.client1js["overall_expenditure"]["planned_expenditure"], 120)

    def test_best_performing(self):
        js = self.js
        self.assertTrue("projects" in self.js)
        projects = self.js["projects"]
        self.assertTrue("best_performing" in projects)
        
        best_performing = projects["best_performing"]
        self.assertEqual(type(best_performing), list)

        self.assertEqual(len(best_performing), 3)
        projects = [self.project3, self.project2, self.project1]
        for i, project in enumerate(projects):
            js = serializers.condensed_project_serializer(project, self.year, self.month)
            js2 = best_performing[i] 
            self.assertEqual(js, js2)

    def test_worst_performing(self):
        js = self.js
        projects = self.js["projects"]
        self.assertTrue("worst_performing" in projects)
        
        worst_performing = projects["worst_performing"]
        self.assertEqual(type(worst_performing), list)

        self.assertEqual(len(worst_performing), 3)
        projects = [self.project1, self.project2, self.project3]
        for i, project in enumerate(projects):
            js = serializers.condensed_project_serializer(project, self.year, self.month)
            js2 = worst_performing[i] 
            self.assertEqual(js, js2)

    def test_projects_per_department(self):
        js = self.js
        self.assertTrue("total_projects" in self.client1js)
        self.assertEqual(self.client1js["total_projects"], 2)

    def test_completed_in_fye(self):
        client = self.client1js
        self.assertIn("projects", client)

        projects = client["projects"]
        self.assertIn("completed_in_fye", projects)

        self.assertEqual(projects["completed_in_fye"], 1)

        projects = self.client2js["projects"]
        self.assertEqual(projects["completed_in_fye"], 0)

    def test_completed_in_fye(self):
        self.assertIn("projects", self.client1js)

        projects = self.client1js["projects"]
        self.assertIn("completed_in_fye", projects)

        self.assertEqual(projects["completed_in_fye"], 1)

        projects = self.client2js["projects"]
        self.assertEqual(projects["completed_in_fye"], 0)

    def test_currently_in_planning(self):
        projects = self.client1js["projects"]
        self.assertEqual(projects["currently_in_planning"], 1)

        projects = self.client2js["projects"]
        self.assertEqual(projects["currently_in_planning"], 0)

    def create_project(self, **kwargs):
        project = factories.ProjectFactory(**kwargs)
        factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.practical_completion(), completion_date=self.dt)
        return project
        
    def test_currently_in_implementation(self):
        project5 = self.create_project(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.practical_completion()
        )

        response = client.get(self.url % (self.project1.municipality.district.id, self.year, self.month))
        js = json.loads(response.content)

        self.assertEqual(js["clients"][0]["projects"]["currently_in_implementation"], 1)
        self.assertEqual(js["clients"][1]["projects"]["currently_in_implementation"], 1)

    def test_currently_in_practical_completion(self):
        project5 = self.create_project(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_completion()
        )

        project6 = self.create_project(
            programme=self.project3.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_completion()
        )

        response = client.get(self.url % (self.project1.municipality.district.id, self.year, self.month))
        js = json.loads(response.content)

        self.assertEqual(js["clients"][0]["projects"]["currently_in_practical_completion"], 2)
        self.assertEqual(js["clients"][1]["projects"]["currently_in_practical_completion"], 1)

    def test_completed_in_final_completion(self):
        project5 = factories.ProjectFactory(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_accounts()
        )
        factories.ProjectMilestoneFactory(project=project5, milestone=models.Milestone.practical_completion(), completion_date=self.dt)

        response = client.get(self.url % (self.project1.municipality.district.id, self.year, self.month))
        js = json.loads(response.content)
        client1js = js["clients"][0]
        client2js = js["clients"][1]

        self.assertEqual(client1js["projects"]["currently_in_final_completion"], 1)
        self.assertEqual(client2js["projects"]["currently_in_final_completion"], 0)
