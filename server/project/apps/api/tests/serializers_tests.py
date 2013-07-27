from django.test import TestCase, Client
from project.apps.api import serializers
from project.apps.projects import factories, models

# TODO do this later
class CondensedProjectSerializerTest(TestCase):
    def setUp(self):
        self.year, self.month = 2013, 6

        self.project = factories.ProjectFactory()
        self.financial = factories.ProjectFinancialFactory(project=self.project)
        self.monthlysubmission = factories.MonthlySubmissionFactory(
            project=self.project, actual_progress=55, actual_expenditure="100", year=self.year, month=self.month
        )
        self.planning = factories.PlanningFactory(
            project=self.project, planned_progress=20, planned_expenses="200", year=self.year, month=self.month
        )

    def test_project_serializer(self):
        js = serializers.condensed_project_serializer(self.project, self.year, self.month)

        self.assertEquals(js["name"], self.project.name)
        self.assertEquals(js["municipality"]["id"], self.project.municipality.id)
        self.assertEquals(js["municipality"]["name"], self.project.municipality.name)
        self.assertEquals(js["district"]["id"], self.project.municipality.district.id)
        self.assertEquals(js["district"]["name"], self.project.municipality.district.name)
        self.assertEquals(js["budget"], self.project.project_financial.total_anticipated_cost)
        self.assertEquals(js["progress"]["actual"], self.project.actual_progress(self.year, self.month))
        self.assertEquals(js["progress"]["planned"], self.project.planned_progress(self.year, self.month))
        self.assertEquals(js["jobs"], self.project.jobs)
        self.assertEquals(js["expenditure"]["ratio"], self.project.project_financial.percentage_expenditure(self.year, self.month))
        self.assertEquals(js["expenditure"]["actual"], self.project.actual_expenditure(self.year, self.month))
        self.assertEquals(js["expenditure"]["planned"], self.project.planned_expenditure(self.year, self.month))
