import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from project.apps.projects import factories, models
import project.apps.api.serializers as serializers
from datetime import datetime
import project.apps.api.reports.district_report
from project.apps.api.reports import graphhelpers

client = Client()

class DistrictTest(TestCase):
    def setUp(self):

        # TODO - not sure why reverse doesn't work
        #self.dashboard_url = reverse("reports_district", kwargs={"district_id" : "1234"})

        self.dashboard_url = "/api/reports/district/%s/%s/%s/"
        self.year, self.month = 2013, 6
        self.date = datetime(self.year, self.month, 1)

        # Both in the same municipality and programme/client
        self.project1 = factories.ProjectFactory(current_step=models.Milestone.tendering_milestone())
        self.programme = self.project1.programme
        self.district = self.project1.municipality.district

        self.project2 = factories.ProjectFactory(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_completion()
        )

        # Same municipality but different programme/client
        self.project3 = factories.ProjectFactory(municipality=self.project1.municipality, current_step=models.Milestone.practical_completion())

        # Same programme different district - doesn't affect total
        self.project4 = factories.ProjectFactory(programme=self.project1.programme)
        self.district2 = self.project4.municipality.district

        self.client1 = self.project1.programme.client
        self.client2 = self.project3.programme.client

        factories.ProjectFinancialFactory(project=self.project1, total_anticipated_cost=100)
        factories.ProjectFinancialFactory(project=self.project2, total_anticipated_cost=50)
        factories.ProjectFinancialFactory(project=self.project3, total_anticipated_cost=60)
        factories.ProjectFinancialFactory(project=self.project4, total_anticipated_cost=200)

        factories.PlanningFactory(project=self.project1, date=self.date, planned_progress=200, planned_expenses="50")
        factories.PlanningFactory(project=self.project2, date=self.date, planned_progress=50, planned_expenses="70")
        factories.PlanningFactory(project=self.project3, date=self.date, planned_progress=25)

        factories.MonthlySubmissionFactory(
            project=self.project1, date=self.date, actual_expenditure=100, actual_progress=80
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project2, date=self.date, actual_expenditure=10, actual_progress=40
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project3, date=self.date, actual_expenditure=300, actual_progress=100
        ) 
        factories.MonthlySubmissionFactory(
            project=self.project4, date=self.date, actual_expenditure=400, actual_progress=20
        ) 

        self.dt = datetime(year=2013, month=6, day=1) 
        self.dt2 = datetime(year=2014, month=6, day=1) 
        factories.ProjectMilestoneFactory(project=self.project1, milestone=models.Milestone.practical_completion(), completion_date=self.dt)
        factories.ProjectMilestoneFactory(project=self.project2, milestone=models.Milestone.practical_completion(), completion_date=self.dt2)
        factories.ProjectMilestoneFactory(project=self.project3, milestone=models.Milestone.practical_completion(), completion_date=self.dt2)
        factories.ProjectMilestoneFactory(project=self.project4, milestone=models.Milestone.practical_completion(), completion_date=self.dt)

        self.reloadjs(self.project1.municipality.district.id)

    def reloadjs(self, district):
        url = self.dashboard_url % (district, self.year, self.month)
        self.response = client.get(url)
        self.assertEquals(self.response.status_code, 200)
        self.js = json.loads(self.response.content)
        self.client1js = self.js["clients"][0]
        self.client2js = self.js["clients"][1]
        return self.js


    def test_district_validates_factory(self):
        response = client.get(self.dashboard_url % (1234, self.year, self.month))
        self.assertEqual(response.status_code, 404)

        response = client.get(self.dashboard_url % (self.project1.municipality.district.id, self.year, self.month))
        self.assertEqual(self.response.status_code, 200)

    def test_district_returns_data(self):
        self.assertEqual(self.js["district"]["name"], self.project1.municipality.district.name)

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
        percentage_expenditure1 = models.Project.objects\
            .client(self.client1)\
            .district(self.district)\
            .percentage_actual_expenditure(self.date) * 100

        self.assertEqual(self.client1js["overall_expenditure"]["perc_expenditure"], percentage_expenditure1)

    def test_actual_expenditure(self):
        self.assertTrue("actual_expenditure" in self.client1js["overall_expenditure"])
        self.assertEqual(self.client1js["overall_expenditure"]["actual_expenditure"], 110)

    def test_planned_expenditure(self):
        self.assertTrue("planned_expenditure" in self.client1js["overall_expenditure"])
        self.assertEqual(self.client1js["overall_expenditure"]["planned_expenditure"], 120)

    def test_best_performing(self):
        brilliant_project_from_another_district = factories.ProjectFactory(name="good project")
        factories.ProjectFinancialFactory(project=brilliant_project_from_another_district, total_anticipated_cost=100)
        factories.PlanningFactory(project=brilliant_project_from_another_district, date=self.date, planned_progress=1)
        factories.MonthlySubmissionFactory(
            project=brilliant_project_from_another_district, date=self.date, actual_progress=100
        ) 

        self.reloadjs(self.project1.municipality.district.id)
        js = self.js

        self.assertTrue("projects" in self.js)
        projects = self.js["projects"]
        self.assertTrue("best_performing" in projects)
        
        best_performing = projects["best_performing"]
        self.assertEqual(type(best_performing), list)

        self.assertEqual(len(best_performing), 3)
        projects = [self.project3, self.project2, self.project1]
        for i, project in enumerate(projects):
            self.assertEquals(project.name, best_performing[i]["name"])

    def test_worst_performing(self):
        terrible_project_from_another_district = factories.ProjectFactory(name="bad project")
        factories.ProjectFinancialFactory(project=terrible_project_from_another_district, total_anticipated_cost=100)
        factories.PlanningFactory(project=terrible_project_from_another_district, date=self.date, planned_progress=100)
        factories.MonthlySubmissionFactory(
            project=terrible_project_from_another_district, date=self.date, actual_progress=0
        ) 

        self.reloadjs(self.project1.municipality.district.id)
        js = self.js
        projects = self.js["projects"]

        self.assertTrue("worst_performing" in projects)
        
        worst_performing = projects["worst_performing"]
        self.assertEqual(type(worst_performing), list)

        self.assertEqual(len(worst_performing), 3)

        projects = [self.project3, self.project2, self.project1]
        projects = [self.project1, self.project2, self.project3]
        for i, project in enumerate(projects):
            self.assertEquals(project.name, worst_performing[i]["name"])

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

        models.Project.objects.all().delete()
        municipality = factories.MunicipalityFactory(district=self.district)

        for i in range(5):
            project = factories.ProjectFactory(programme=self.programme, municipality=municipality)
            factories.ProjectMilestoneFactory(
                completion_date=datetime(2013, 6, 1), milestone=models.Milestone.practical_completion(), project=project
            )
            project = factories.ProjectFactory(programme=self.programme, municipality=municipality)
            factories.ProjectMilestoneFactory(
                completion_date=datetime(2014, 6, 1), milestone=models.Milestone.practical_completion(), project=project
            )

        js = self.reloadjs(self.project1.municipality.district.id)
        clientjs = self.client1js
        
        self.assertIn("projects", clientjs)

        projects = clientjs["projects"]
        self.assertIn("completed_in_fye", projects)

        self.assertEqual(projects["completed_in_fye"], 5)

        projects = self.client2js["projects"]
        self.assertEqual(projects["completed_in_fye"], 0)

    def test_currently_in_planning(self):
        projects = self.client1js["projects"]
        self.assertEqual(projects["currently_in_planning"], 1)

        projects = self.client2js["projects"]
        self.assertEqual(projects["currently_in_planning"], 0)

    def test_currently_in_implementation(self):
        models.Project.objects.all().delete()

        js = self.reloadjs(self.project1.municipality.district.id)
        self.assertEqual(js["clients"][0]["projects"]["currently_in_implementation"], 0)
        self.assertEqual(js["clients"][1]["projects"]["currently_in_implementation"], 0)

        project5 = factories.ProjectFactory(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.practical_completion()
        )

        js = self.reloadjs(self.project1.municipality.district.id)

        self.assertEqual(js["clients"][0]["projects"]["currently_in_implementation"], 1)
        self.assertEqual(js["clients"][1]["projects"]["currently_in_implementation"], 0)

    def test_currently_in_practical_completion(self):
        models.Project.objects.all().delete()

        js = self.reloadjs(self.project1.municipality.district.id)
        self.assertEqual(js["clients"][0]["projects"]["currently_in_practical_completion"], 0)
        self.assertEqual(js["clients"][1]["projects"]["currently_in_practical_completion"], 0)

        project5 = factories.ProjectFactory(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_completion()
        )

        project6 = factories.ProjectFactory(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_completion()
        )

        project7 = factories.ProjectFactory(
            programme=self.project3.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_completion()
        )

        js = self.reloadjs(self.project1.municipality.district.id)

        self.assertEqual(js["clients"][0]["projects"]["currently_in_practical_completion"], 2)
        self.assertEqual(js["clients"][1]["projects"]["currently_in_practical_completion"], 1)

    def test_completed_in_final_completion(self):
        project5 = factories.ProjectFactory(
            programme=self.project1.programme,
            municipality=self.project1.municipality,
            current_step=models.Milestone.final_accounts()
        )
        factories.ProjectMilestoneFactory(project=project5, milestone=models.Milestone.practical_completion(), completion_date=self.dt)

        response = client.get(self.dashboard_url % (self.project1.municipality.district.id, self.year, self.month))
        js = json.loads(response.content)
        client1js = js["clients"][0]
        client2js = js["clients"][1]

        self.assertEqual(client1js["projects"]["currently_in_final_completion"], 1)
        self.assertEqual(client2js["projects"]["currently_in_final_completion"], 0)

    def test_actual_progress(self):
        models.Project.objects.all().delete()
        year, month = 2013, 6
        programme = factories.ProgrammeFactory()
        municipality = factories.MunicipalityFactory()

        
        for i in range(10):
            project = factories.ProjectFactory(programme=programme, municipality=municipality)
            planning = factories.PlanningFactory(project=project, planned_progress=10*i, date=self.date)
            submission = factories.MonthlySubmissionFactory(project=project, actual_progress=10*i, date=self.date)
            financial = factories.ProjectFinancialFactory(project=project)

        district = project.municipality.district
        js = self.reloadjs(district.id)

        client = programme.client

        self.assertTrue("between_0_and_50" in js["clients"][2]["projects"])
        self.assertEqual(js["clients"][2]["projects"]["between_0_and_50"], 5)
        self.assertTrue("between_51_and_75" in js["clients"][2]["projects"])
        self.assertEqual(js["clients"][2]["projects"]["between_51_and_75"], 2)
        self.assertTrue("between_76_and_99" in js["clients"][2]["projects"])
        self.assertEqual(js["clients"][2]["projects"]["between_76_and_99"], 2)


class TestGraphHelpers(TestCase):
    def test_dashboard_gauge(self):
        gauge2 = graphhelpers.dashboard_gauge(1, 1)
        self.assertEqual(gauge2[0]["text"], "Planned")
        self.assertEqual(gauge2[1]["text"], "Actual")

        gauge3 = graphhelpers.dashboard_gauge(1, 1, text1="abc", text2="def")
        self.assertEqual(gauge3[0]["text"], "abc")
        self.assertEqual(gauge3[1]["text"], "def")

    def test_dashboard_slider(self):
        slider1 = graphhelpers.dashboard_slider(0, 0, "DoE")
        self.assertEqual(slider1[0]["position"], 0.1)
        self.assertEqual(slider1[1]["position"], 0.1)

        slider2 = graphhelpers.dashboard_slider(1, 1, "DoE")
        self.assertEqual(slider2[0]["position"], 0.8)
        self.assertEqual(slider2[1]["position"], 0.8)

        slider3 = graphhelpers.dashboard_slider(0.5, 0.7, "DoE")
        self.assertEqual(slider3[0]["marker-text"], "Planned")
        self.assertEqual(slider3[1]["marker-text"], "Actual")
        slider3 = graphhelpers.dashboard_slider(0.5, 0.7, "DoE", text1="aaa", text2="bbb")
        self.assertEqual(slider3[0]["marker-text"], "aaa")
        self.assertEqual(slider3[1]["marker-text"], "bbb")

        slider4 = graphhelpers.dashboard_slider(0.7, 0.5, "DoE", threshold=0.5)
        self.assertEqual(slider4[0]["bar-color"], graphhelpers.clientcolors["DoE"])
        self.assertEqual(slider4[1]["bar-color"], graphhelpers.clientcolors["DoE"])

        slider5 = graphhelpers.dashboard_slider(0.7, 0.5, "DoE", threshold=0.1)
        self.assertEqual(slider5[1]["bar-color"], graphhelpers.red)
        self.assertEqual(slider5[0]["bar-color"], graphhelpers.clientcolors["DoE"])

        slider6 = graphhelpers.dashboard_slider(0.5, 0.7, "DoE", threshold=0.1)
        self.assertEqual(slider6[0]["bar-color"], graphhelpers.clientcolors["DoE"])
        self.assertEqual(slider6[1]["bar-color"], graphhelpers.red)

        
        slider7 = graphhelpers.dashboard_slider(0.5, 0.55, "DoE", threshold=0.1)
        self.assertEqual(slider7[0]["marker-text"], "")


class GraphJson(TestCase):
    def setUp(self):
        self.municipality = factories.MunicipalityFactory()
        self.district = self.municipality.district
        self.year, self.month = 2013, 6
        self.url = reverse("api:reports:district_graphs", args=(self.district.id, self.year, self.month))
        self.date = datetime(self.year, self.month, 1)

        for i in range(5):
            project = factories.ProjectFactory(municipality=self.municipality)
            submission = factories.MonthlySubmissionFactory(project=project, actual_progress=i*10, actual_expenditure=i*10, date=self.date)
            planning = factories.PlanningFactory(project=project, planned_progress=i*20, planned_expenses=i*20, date=self.date)
            factories.ProjectFinancialFactory(project=project, total_anticipated_cost=10)

        self.response = client.get(self.url)
        self.js = json.loads(self.response.content)

    def test_gauges(self):

        self.assertEqual(self.response.status_code, 200)

        for i in range(0, 5):
            gauge = "gauge%d" % (i + 1)
            self.assertIn(gauge, self.js)
            self.assertEqual(self.js[gauge][0]["position"], (i * 2) / 10.)
            self.assertEqual(self.js[gauge][1]["position"], i / 10.)

    def test_sliders(self):

        for i in range(0, 5):
            slider = "slider%d" % (i + 1)
            self.assertIn(slider, self.js)
            if i == 0:
                self.assertEqual(self.js[slider][0]["position"], 0.1)
                self.assertEqual(self.js[slider][1]["position"], 0.1)
            else:
                # Values should swap around because the position of the sliders
                # swaps if val1 > val 2
                self.assertEqual(self.js[slider][0]["position"], i / 10.)
                self.assertEqual(self.js[slider][1]["position"], (i * 2) / 10.)
    # TODO add tests to test budget calculations for slider and also when budget is 0
