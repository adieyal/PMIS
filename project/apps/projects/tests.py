from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import factories, models

class FinancialYearTest(TestCase):
    def setUp(self):
        self.project = factories.ProjectFactory.create()
        for i in range(1, 13):
            self.planning = factories.PlanningFactory.create(year="2013", month=str(i), project=self.project)

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
