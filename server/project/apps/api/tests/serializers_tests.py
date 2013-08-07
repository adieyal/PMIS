from django.test import TestCase, Client
from datetime import datetime
from project.apps.api import serializers
from project.apps.projects import factories, models

# TODO do this later
class CondensedProjectSerializerTest(TestCase):
    def setUp(self):
        self.year, self.month = 2013, 6
        self.date = datetime(self.year, self.month, 1)

        self.project = factories.ProjectFactory()
        self.financial = factories.ProjectFinancialFactory(project=self.project)
        self.monthlysubmission = factories.MonthlySubmissionFactory(
            project=self.project, actual_progress=55, actual_expenditure="100", date=self.date
        )
        self.planning = factories.PlanningFactory(
            project=self.project, planned_progress=20, planned_expenses="200", date=self.date
        )

    def test_project_serializer(self):
        js = serializers.condensed_project_serializer(self.project, self.date)

        self.assertEquals(js["name"], self.project.name)
        self.assertEquals(js["client"], self.project.programme.client.name)
        self.assertEquals(js["municipality"]["id"], self.project.municipality.id)
        self.assertEquals(js["municipality"]["name"], self.project.municipality.name)
        self.assertEquals(js["district"]["id"], self.project.municipality.district.id)
        self.assertEquals(js["district"]["name"], self.project.municipality.district.name)
        self.assertEquals(js["budget"], self.project.project_financial.total_anticipated_cost)
        self.assertEquals(js["progress"]["actual"], self.project.actual_progress(self.date))
        self.assertEquals(js["progress"]["planned"], self.project.planned_progress(self.date))
        self.assertEquals(js["jobs"], self.project.jobs)
        self.assertEquals(js["expenditure"]["perc_spent"], self.project.project_financial.percentage_expenditure(self.date) * 100)
        self.assertEquals(js["expenditure"]["actual"], self.project.actual_expenditure(self.date))
        self.assertEquals(js["expenditure"]["planned"], self.project.planned_expenditure(self.date))

class ExpandedProjectSerializerTest(TestCase):
    def setUp(self):
        self.year, self.month = 2013, 6
        self.pyear, self.pmonth = 2013, 5
        self.date = datetime(self.year, self.month, 1)
        self.pdate = datetime(self.pyear, self.pmonth, 1)

        self.project = factories.ProjectFactory()
        self.financial = factories.ProjectFinancialFactory(project=self.project)
        self.monthlysubmission = factories.MonthlySubmissionFactory(
            project=self.project, actual_progress=55, actual_expenditure="100", date=self.date,
            comment="This Month Comment", remedial_action="This Month Mitigation"
        )

        self.monthlysubmission2 = factories.MonthlySubmissionFactory(
            project=self.project, actual_progress=55, actual_expenditure="100", date=self.pdate,
            comment="Last Month Comment", remedial_action="Last Month Mitigation"
        )
        self.planning = factories.PlanningFactory(
            project=self.project, planned_progress=20, planned_expenses="200", date=self.date
        )

        factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.start_milestone())
        factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.practical_completion())
        factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.final_completion())
        factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.final_accounts())


    def test_project_serializer(self):
        js = serializers.expanded_project_serializer(self.project, self.date)
        self.assertEquals(js["milestones"]["start_date"], self.project.start_milestone.completion_date) 
        self.assertEquals(js["milestones"]["practical_completion"], self.project.practical_completion_milestone.completion_date) 
        self.assertEquals(js["milestones"]["final_completion"], self.project.final_completion_milestone.completion_date) 
        self.assertEquals(js["milestones"]["final_accounts"], self.project.final_accounts_milestone.completion_date) 
        self.assertEquals(js["last_month"]["comment"], "Last Month Comment")
        self.assertEquals(js["last_month"]["mitigation"], "Last Month Mitigation")
        self.assertEquals(js["current_month"]["comment"], "This Month Comment")
        self.assertEquals(js["current_month"]["mitigation"], "This Month Mitigation")
