from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import factories
import project.apps.projects.models as models

class CalendarFunctionsTest(TestCase):
    def setUp(self):
        self.year = 2013
        self.month = 5
    def test_previous_year(self):
        self.assertEquals(models.CalendarFunctions.previous_year(self.year, self.month), (2012, 5))

    def test_next_year(self):
        self.assertEquals(models.CalendarFunctions.next_year(self.year, self.month), (2014, 5))

    def test_previous_month(self):
        self.assertEquals(models.CalendarFunctions.previous_month(self.year, self.month), (2013, 4))
        self.assertEquals(models.CalendarFunctions.previous_month(self.year, 1), (2012, 12))

    def test_next_month(self):
        self.assertEquals(models.CalendarFunctions.next_month(self.year, self.month), (2013, 6))
        self.assertEquals(models.CalendarFunctions.next_month(self.year, 12), (2014, 1))
        

class FinancialYearTest(TestCase):
    def setUp(self):
        self.project = factories.ProjectFactory.create()
        for i in range(1, 13):
            self.planning = factories.PlanningFactory.create(
                year="2013", month=str(i), project=self.project
            )

    def test_financial_year(self):
        
        planning_2013 = models.Planning.objects.in_financial_year("2013")
        planning_2014 = models.Planning.objects.in_financial_year("2014")

        self.assertEquals(planning_2013.count(), 3)
        self.assertEquals(planning_2014.count(), 9)
        for p in planning_2013:
            self.assertTrue(p.month in ["1", "2", "3"])

        for p in planning_2014:
            self.assertTrue(p.month in ["4", "5", "6", "7", "8", "9", "10", "11", "12"])

class ProjectManagerTest(TestCase):
    def setUp(self):
        self.client = factories.ClientFactory.create()
        self.programme = factories.ProgrammeFactory.create(client=self.client)
        self.district = factories.DistrictFactory.create()
        self.municipality = factories.MunicipalityFactory.create(district=self.district)
        self.project = factories.ProjectFactory.create(municipality=self.municipality, programme=self.programme)

    def test_client(self):
        projects = self.project.objects.client(self.client)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0].programme.client, self.client)

    def test_municipality(self):
        projects = models.Project.objects.municipality(self.municipality)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0].municipality.district, self.district)

    def test_district(self):
        projects = models.Project.objects.district(self.district)
        self.assertEquals(len(projects), 1)
        
    def test_client(self):
        projects = models.Project.objects.client(self.client)
        self.assertEquals(len(projects), 1)

class ProjectFinancialTest(TestCase):
    def test_percentage_expenditure(self):
        project = factories.ProjectFactory()
        financial = factories.ProjectFinancialFactory(project=project, total_anticipated_cost=100)
        actual = factories.MonthlySubmissionFactory(
            project=project, actual_expenditure=25, year=2013, month=6
        )
        self.assertEquals(financial.percentage_expenditure(2013, 6), 25)
        self.assertRaises(models.ProjectException, financial.percentage_expenditure, 2013, 7)

        financial.total_anticipated_cost = 0
        financial.save()
        self.assertRaises(models.ProjectException, financial.percentage_expenditure, 2013, 6)

class ProjectTest(TestCase):
    def setUp(self):
        performance = range(0, 100, 10)
        self.projects = []
        self.year, self.month = 2013, 6
        
        for p in performance:
            project = factories.ProjectFactory()
            self.projects.append(project)
            factories.PlanningFactory(project=project, planned_progress=50, year=self.year, month=self.month)
            factories.MonthlySubmissionFactory(project=project, actual_progress=p, year=self.year, month=self.month)

        
    def test_project_actual_progress(self):
        project = self.projects[2]
        self.assertEquals(project.actual_progress(self.year, self.month), 20)
        self.assertRaises(models.ProjectException, project.actual_progress, 2012, 3)

    def test_project_planned_progress(self):
        project = self.projects[2]
        self.assertEquals(project.planned_progress(self.year, self.month), 50)
        self.assertRaises(models.ProjectException, project.planned_progress, 2012, 3)

    def test_project_performance(self):
        project = self.projects[2]
        self.assertEquals(project.performance(self.year, self.month), 20/50.)


        zero_planning_project = factories.ProjectFactory()
        factories.PlanningFactory(project=zero_planning_project, planned_progress=0, year=self.year, month=self.month)
        factories.MonthlySubmissionFactory(project=zero_planning_project, actual_progress=0, year=self.year, month=self.month)
        self.assertEquals(zero_planning_project.performance(self.year, self.month), 0)

    def test_best_performing(self):
        best = models.Project.objects.best_performing(self.year, self.month, count=5)
        self.assertEquals(len(best), 5)
        for i, actual in enumerate(range(90, 0, -10)[0:5]):
            project = best[i]
            expected_performance = actual / 50.
            self.assertEquals(project.performance(self.year, self.month), expected_performance)
        
    
    def test_worst_performing(self):
        worst = models.Project.objects.worst_performing(self.year, self.month, count=5)
        self.assertEquals(len(worst), 5)
        for i, actual in enumerate(range(0, 100, -10)[0:5]):
            project = worst[i]
            expected_performance = actual / 50.
            self.assertEquals(project.performance(self.year, self.month), expected_performance)
