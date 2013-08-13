from __future__ import division
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import factories
import project.apps.projects.models as models
from datetime import datetime

class CalendarFunctionsTest(TestCase):
    def setUp(self):
        self.year = 2013
        self.month = 5
    def test_previous_year(self):
        self.assertEqual(models.CalendarFunctions.previous_year(self.year, self.month), (2012, 5))

    def test_next_year(self):
        self.assertEqual(models.CalendarFunctions.next_year(self.year, self.month), (2014, 5))

    def test_previous_month(self):
        self.assertEqual(models.CalendarFunctions.previous_month(self.year, self.month), (2013, 4))
        self.assertEqual(models.CalendarFunctions.previous_month(self.year, 1), (2012, 12))

    def test_next_month(self):
        self.assertEqual(models.CalendarFunctions.next_month(self.year, self.month), (2013, 6))
        self.assertEqual(models.CalendarFunctions.next_month(self.year, 12), (2014, 1))

class TestMilestone(TestCase):
    def test_milestones_loaded(self):
        self.assertEqual(models.Milestone.objects.count(), 9)

    def test_milestone_names(self):
        self.assertEqual(models.Milestone.start_milestone().name, "Project Identification")
        self.assertEqual(models.Milestone.practical_completion().name, "Practical Completion")
        self.assertEqual(models.Milestone.final_completion().name, "Final Completion")
        self.assertEqual(models.Milestone.final_accounts().name, "Final Accounts")

class TestProjectMilestone(TestCase):
    def setUp(self):
        self.project = factories.ProjectFactory.create()
        self.start_milestone = factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.start_milestone())
        self.practical_completion = factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.practical_completion())
        self.final_completion = factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.final_completion())
        self.final_accounts = factories.ProjectMilestoneFactory(project=self.project, milestone=models.Milestone.final_accounts())

    def test_project_start_milestone(self):
        self.assertEqual(models.ProjectMilestone.objects.project_start(self.project), self.start_milestone)

    def test_project_practical_completion_milestone(self):
        self.assertEqual(models.ProjectMilestone.objects.project_practical_completion(self.project), self.practical_completion)

    def test_project_final_completion_milestone(self):
        self.assertEqual(models.ProjectMilestone.objects.project_final_completion(self.project), self.final_completion)

    def test_project_final_accounts_milestone(self):
        self.assertEqual(models.ProjectMilestone.objects.project_final_accounts(self.project), self.final_accounts)

class FinancialYearTest(TestCase):
    def setUp(self):
        self.project = factories.ProjectFactory.create()
        for i in range(1, 13):
            self.planning = factories.PlanningFactory.create(
                date=datetime(2013, i, 1), project=self.project
            )

    def test_financial_year(self):
        
        planning_2013 = models.Planning.objects.in_financial_year(datetime(2013, 1, 1))
        planning_2014 = models.Planning.objects.in_financial_year(datetime(2014, 1, 1))

        self.assertEqual(planning_2013.count(), 3)
        self.assertEqual(planning_2014.count(), 9)
        for p in planning_2013:
            self.assertTrue(p.date.month in [1, 2, 3])

        for p in planning_2014:
            self.assertTrue(p.date.month in [4, 5, 6, 7, 8, 9, 10, 11, 12])

    def test_which_year(self):
        self.assertEqual(models.FinancialYearManager.financial_year(2013, 2), 2013)
        self.assertEqual(models.FinancialYearManager.financial_year(2013, 4), 2014)

    def test_date_in_financial_year(self):
        dt = datetime(2013, 6, 1)

        self.assertTrue(models.FinancialYearManager.date_in_financial_year(2014, dt))
        self.assertFalse(models.FinancialYearManager.date_in_financial_year(2013, dt))

        self.assertTrue(models.FinancialYearManager.yearmonth_in_financial_year(2014, 2013, 6))
        self.assertFalse(models.FinancialYearManager.yearmonth_in_financial_year(2013, 2013, 6))

    def test_start_of_year(self):
        dt = models.FinancialYearManager.start_of_year(2014)
        self.assertEqual(dt.year, 2013)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 1)

        dt = models.FinancialYearManager.start_of_year(2013)
        self.assertEqual(dt.year, 2012)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 1)

    def test_end_of_year(self):
        dt = models.FinancialYearManager.end_of_year(2014)
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 3)
        self.assertEqual(dt.day, 31)
        

class ProjectManagerTest(TestCase):
    def setUp(self):
        self.client = factories.ClientFactory.create()
        self.programme = factories.ProgrammeFactory.create(client=self.client)
        self.district = factories.DistrictFactory.create()
        self.municipality = factories.MunicipalityFactory.create(district=self.district)
        self.project = factories.ProjectFactory.create(municipality=self.municipality, programme=self.programme)

    def test_client(self):
        projects = self.project.objects.client(self.client)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].programme.client, self.client)

    def test_municipality(self):
        projects = models.Project.objects.municipality(self.municipality)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].municipality.district, self.district)

    def test_district(self):
        projects = models.Project.objects.district(self.district)
        self.assertEqual(len(projects), 1)
        
    def test_client(self):
        projects = models.Project.objects.client(self.client)
        self.assertEqual(len(projects), 1)

    def test_projects_by_progress(self):
        models.Project.objects.all().delete()
        year, month = 2013, 6
        date = datetime(year, month, 1)
        for i in range(10):
            project = factories.ProjectFactory()
            planning = factories.PlanningFactory(project=project, planned_progress=10*i, date=date)
            submission = factories.MonthlySubmissionFactory(project=project, actual_progress=10*i, date=date)

        low_performance_projects = models.Project.objects.actual_progress_between(0, 50)
        
        self.assertEquals(len(low_performance_projects), 5)
        for project in low_performance_projects:
            self.assertTrue(project.actual_progress(date) >= 0)
            self.assertTrue(project.actual_progress(date) < 50)

        low_performance_projects = models.Project.objects.planned_progress_between(0, 50)
        self.assertEquals(len(low_performance_projects), 5)
        for project in low_performance_projects:
            self.assertTrue(project.planned_progress(date) >= 0)
            self.assertTrue(project.planned_progress(date) < 50)

        high_performance_projects = models.Project.objects.actual_progress_between(50, 100)
        self.assertEquals(len(high_performance_projects), 5)
        for project in high_performance_projects:
            self.assertTrue(project.actual_progress(date) >= 50)
            self.assertTrue(project.actual_progress(date) < 100)

        high_performance_projects = models.Project.objects.planned_progress_between(50, 100)
        self.assertEquals(len(high_performance_projects), 5)
        for project in high_performance_projects:
            self.assertTrue(project.planned_progress(date) >= 50)
            self.assertTrue(project.planned_progress(date) < 100)

    def test_projects_completed_in_fye(self):
        models.Project.objects.all().delete()
        year, month = 2013, 6
        date = datetime(year, month, 1)
        for i in range(5):
            project = factories.ProjectFactory()
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.practical_completion(), completion_date=datetime(2013, 6, 1))

            project = factories.ProjectFactory()
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.practical_completion(), completion_date=datetime(2014, 6, 1))

        completed_2014 = models.Project.objects.completed_by_fye(2014)
        self.assertEquals(len(completed_2014), 5)
        for p in completed_2014:
            self.assertEquals(p.practical_completion_milestone.completion_date.year, 2013)
            self.assertEquals(p.practical_completion_milestone.completion_date.month, 6)

        completed_2015 = models.Project.objects.completed_by_fye(2015)
        self.assertEquals(len(completed_2015), 5)
        for p in completed_2015:
            self.assertEquals(p.practical_completion_milestone.completion_date.year, 2014)
            self.assertEquals(p.practical_completion_milestone.completion_date.month, 6)

    def test_projects_completed_in_fye_different_clients(self):
        models.Project.objects.all().delete()
        year, month = 2013, 6
        date = datetime(2013, 6, 1)

        prog1 = factories.ProgrammeFactory()
        prog2 = factories.ProgrammeFactory()

        for i in range(5):
            project = factories.ProjectFactory(programme=prog1)
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.practical_completion(), completion_date=date)

            project = factories.ProjectFactory(programme=prog2)
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.practical_completion(), completion_date=date)

        completed_client1 = models.Project.objects.client(prog1.client).completed_by_fye(2014)
        self.assertEquals(len(completed_client1), 5)
        for p in completed_client1:
            self.assertEquals(p.practical_completion_milestone.completion_date.year, year)
            self.assertEquals(p.practical_completion_milestone.completion_date.month, month)

        completed_client2 = models.Project.objects.client(prog2.client).completed_by_fye(2014)
        self.assertEquals(len(completed_client2), 5)
        for p in completed_client2:
            self.assertEquals(p.practical_completion_milestone.completion_date.year, year)
            self.assertEquals(p.practical_completion_milestone.completion_date.month, month)

class ProjectFinancialTest(TestCase):
    def test_percentage_expenditure(self):
        date = datetime(2013, 6, 1)
        date2 = datetime(2013, 7, 1)
        project = factories.ProjectFactory()
        financial = factories.ProjectFinancialFactory(project=project, total_anticipated_cost=80)
        actual = factories.MonthlySubmissionFactory(project=project, actual_expenditure=25, date=date)
        self.assertEqual(financial.percentage_expenditure(date), 31.25)
        self.assertEqual(financial.percentage_expenditure(date2), 31.25)

        factories.MonthlySubmissionFactory(project=project, actual_expenditure=50, date=date2)
        self.assertEqual(financial.percentage_expenditure(date2), 93.75)

        financial.total_anticipated_cost = 0
        financial.save()
        self.assertEqual(financial.percentage_expenditure(date), 0)

class TestProject(TestCase):
    def setUp(self):
        performance = range(0, 100, 10)
        self.projects = []
        self.year, self.month = 2013, 6
        self.munic1 = factories.MunicipalityFactory() 
        self.munic2 = factories.MunicipalityFactory() 
        self.date = datetime(self.year, self.month, 1)

        for idx, p in enumerate(performance):
            project = factories.ProjectFactory(municipality=self.munic1 if idx < 5 else self.munic2)
            self.projects.append(project)
            planning = factories.PlanningFactory(project=project, planned_progress=50, planned_expenses=(100 * idx), date=self.date)
            factories.MonthlySubmissionFactory(project=project, actual_progress=p, actual_expenditure=(200 * idx), date=self.date)
            factories.ProjectFinancialFactory(project=project, total_anticipated_cost=100 * idx)
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.start_milestone())
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.practical_completion())
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.final_completion())
            factories.ProjectMilestoneFactory(project=project, milestone=models.Milestone.final_accounts())

        
    def test_project_actual_progress(self):
        date1 = datetime(2013, 6, 1)
        date2 = datetime(2013, 7, 1)
        date3 = datetime(2013, 8, 1)
        models.Project.objects.all().delete()
        project = factories.ProjectFactory()
        self.assertEqual(project.actual_progress(date1), 0)

        factories.MonthlySubmissionFactory(project=project, actual_progress=54, date=date1)
        factories.MonthlySubmissionFactory(project=project, actual_progress=82, date=date2)

        self.assertEqual(project.actual_progress(date1), 54)
        self.assertEqual(project.actual_progress(date2), 82)
        # If a submission does not exist - assume the progress is the same as the last progress
        self.assertEqual(project.actual_progress(date3), 82)

    def test_project_planned_progress(self):
        date1 = datetime(2013, 6, 1)
        date2 = datetime(2013, 7, 1)
        date3 = datetime(2013, 8, 1)
        models.Project.objects.all().delete()
        project = factories.ProjectFactory()
        self.assertRaises(models.ProjectException, project.planned_progress, datetime(2012, 3, 1))

        factories.PlanningFactory(project=project, planned_progress=54, date=date1)
        factories.PlanningFactory(project=project, planned_progress=82, date=date2)

        self.assertEqual(project.planned_progress(date1), 54)
        self.assertEqual(project.planned_progress(date2), 82)
        # If a submission does not exist - assume the progress is the same as the last progress
        self.assertEqual(project.planned_progress(date3), 82)

    def test_project_performance(self):
        project = self.projects[2]
        self.assertEqual(project.performance(self.date), 20/50.)


        zero_planning_project = factories.ProjectFactory()
        factories.PlanningFactory(project=zero_planning_project, planned_progress=0, date=self.date)
        factories.MonthlySubmissionFactory(project=zero_planning_project, actual_progress=0, date=self.date)
        self.assertEqual(zero_planning_project.performance(self.date), 0)

    def test_best_performing(self):
        best = models.Project.objects.best_performing(self.date, count=5)
        self.assertEqual(len(best), 5)
        for i, actual in enumerate(range(90, 0, -10)[0:5]):
            project = best[i]
            expected_performance = actual / 50.
            self.assertEqual(project.performance(self.date), expected_performance)
        
    
    def test_worst_performing(self):
        worst = models.Project.objects.worst_performing(date=self.date, count=5)
        self.assertEqual(len(worst), 5)
        for i, actual in enumerate(range(0, 100, -10)[0:5]):
            project = worst[i]
            expected_performance = actual / 50.
            self.assertEqual(project.performance(self.date), expected_performance)

    def test_worst_performing_with_different_months(self):
        new_date = datetime(self.year + 1, self.month, 1)
        new_project = factories.ProjectFactory(municipality=self.munic1)
        factories.PlanningFactory(project=new_project, planned_progress=100, date=new_date)
        factories.MonthlySubmissionFactory(project=new_project, actual_progress=10, date=new_date)

        worst = models.Project.objects.worst_performing(date=self.date, count=100)
        self.assertEqual(len(worst), 10)
        for p in worst:
            self.assertNotEquals(new_project, worst)

    def test_best_and_worst_can_work_on_filter(self):
        best = models.Project.objects.municipality(self.munic1).best_performing(self.date, count=5)
        for idx, actual in enumerate(range(40, 0, -10)[0:5]):
            project = best[idx]
            self.assertEqual(project.performance(self.date), actual / 50.)
        
        best = models.Project.objects.municipality(self.munic2).best_performing(self.date, count=5)
        for idx, actual in enumerate(range(90, 0, -10)[0:5]):
            project = best[idx]
            self.assertEqual(project.performance(self.date), actual / 50.)

        worst = models.Project.objects.municipality(self.munic1).worst_performing(self.date, count=5)
        for idx, actual in enumerate(range(0, 50, 10)[0:5]):
            project = worst[idx]
            self.assertEqual(project.performance(self.date), actual / 50.)
        
        worst = models.Project.objects.municipality(self.munic2).worst_performing(self.date, count=5)
        for idx, actual in enumerate(range(50, 100, 10)[0:5]):
            project = worst[idx]
            self.assertEqual(project.performance(self.date), actual / 50.)

    def test_actual_expenditure(self):
        date1 = datetime(2013, 6, 1)
        date2 = datetime(2013, 7, 1)
        models.Project.objects.all().delete()
        project = factories.ProjectFactory()
        self.assertEqual(project.actual_expenditure(date1), 0)

        factories.MonthlySubmissionFactory(project=project, actual_expenditure=100, date=date1)
        factories.MonthlySubmissionFactory(project=project, actual_expenditure=200, date=date2)

        self.assertEqual(project.actual_expenditure(date1), 100)
        self.assertEqual(project.actual_expenditure(date2), 300)

    def test_actual_expenditure_with_previous_expenses(self):
        date1 = datetime(2013, 6, 1)
        date2 = datetime(2013, 7, 1)
        models.Project.objects.all().delete()
        project = factories.ProjectFactory()

        factories.MonthlySubmissionFactory(project=project, actual_expenditure=100, date=date1)
        factories.MonthlySubmissionFactory(project=project, actual_expenditure=200, date=date2)
        factories.ProjectFinancial(project=project, previous_expenses=500)

        self.assertEqual(project.actual_expenditure_overall(), 800)
        
    def test_planned_expenditure(self):

        date1 = datetime(2013, 6, 1)
        date2 = datetime(2013, 7, 1)
        models.Project.objects.all().delete()
        project = factories.ProjectFactory()
        self.assertEqual(project.planned_expenditure(date1), 0)

        factories.PlanningFactory(project=project, planned_expenses=100, date=date1)
        factories.PlanningFactory(project=project, planned_expenses=200, date=date2)

        self.assertEqual(project.planned_expenditure(date1), 100)
        self.assertEqual(project.planned_expenditure(date2), 300)

        #project = self.projects[0]
        #self.assertEqual(project.planned_expenditure(self.date), 0)

        #project = self.projects[1]
        #self.assertEqual(project.planned_expenditure(self.date), 100)

    def test_start_date(self):
        project = self.projects[0]
        self.assertEqual(project.start_milestone, models.ProjectMilestone.objects.project_start(project))

    def test_practical_completion(self):
        project = self.projects[0]
        self.assertEqual(project.practical_completion_milestone, models.ProjectMilestone.objects.project_practical_completion(project))

    def test_final_completion(self):
        project = self.projects[0]
        self.assertEqual(project.final_completion_milestone, models.ProjectMilestone.objects.project_final_completion(project))

    def test_final_accounts(self):
        project = self.projects[0]
        self.assertEqual(project.final_accounts_milestone, models.ProjectMilestone.objects.project_final_accounts(project))

    def test_average_progress(self):
        models.Project.objects.all().delete()
        date1 = datetime(2013, 5, 1)
        date2 = datetime(2013, 6, 1)

        self.assertEqual(models.Project.objects.average_actual_progress(date1), 0)
        progress = []
        for i in range(5):
            project = factories.ProjectFactory()
            factories.MonthlySubmissionFactory(project=project, actual_progress=i*10, date=date1)
            factories.PlanningFactory(project=project, planned_progress=i*20, date=date1)
            progress.append(i * 10)

        projects = models.Project.objects.all()
        avg_progress = sum(progress) / len(progress)
        self.assertEqual(projects.average_actual_progress(date1), avg_progress)
        self.assertEqual(projects.average_planned_progress(date1), avg_progress * 2)

    def test_total_budget(self):
        projects = models.Project.objects.district(self.munic1.district)
        total = sum([p.project_financial.total_anticipated_cost for p in projects])
        
        self.assertEqual(projects.total_budget(), total)

        models.Project.objects.all().delete()
        project = factories.ProjectFactory()
        self.assertEqual(models.Project.objects.all().total_budget(), 0)

    def test_total_actual_expenditure(self):
        models.Project.objects.all().delete()
        date1 = datetime(2013, 5, 1)
        date2 = datetime(2013, 6, 1)

        self.assertEqual(models.Project.objects.total_actual_expenditure(date1), 0)
        for i in range(5):
            project = factories.ProjectFactory()
            factories.MonthlySubmissionFactory(project=project, actual_expenditure=100, date=date1)
            factories.MonthlySubmissionFactory(project=project, actual_expenditure=100, date=date2)

        # Should include only may expenditure
        projects = models.Project.objects.all()
        total = sum([p.actual_expenditure(date1) for p in projects])
        self.assertEqual(projects.total_actual_expenditure(date1), total)

        # Should include both may and june expenditure
        total = sum([p.actual_expenditure(date2) for p in projects])
        self.assertEqual(projects.total_actual_expenditure(date2), total)

        # Check that subsets are catered for - i.e. not just .all()
        district = projects[0].municipality.district
        projects = models.Project.objects.district(district)
        total = sum([p.actual_expenditure(date1) for p in projects])
        self.assertEqual(projects.total_actual_expenditure(date1), total)
        total = sum([p.actual_expenditure(date2) for p in projects])
        self.assertEqual(projects.total_actual_expenditure(date2), total)

    def test_previous_expenditure(self):
        models.Project.objects.all().delete()
        date1 = datetime(2013, 5, 1)
        date2 = datetime(2013, 6, 1)

        for i in range(5):
            project = factories.ProjectFactory()
            factories.MonthlySubmissionFactory(project=project, actual_expenditure=100, date=date1)
            factories.MonthlySubmissionFactory(project=project, actual_expenditure=100, date=date2)
            factories.ProjectFinancialFactory(project=project, previous_expenses=1000)

        # Test expenditure using previous expenditure as well

        projects = models.Project.objects.all()
        total = sum([p.actual_expenditure_overall() for p in projects])
        self.assertEqual(projects.total_actual_expenditure_overall(), total)
        
    def test_total_planned_expenditure(self):
        models.Project.objects.all().delete()

        date1 = datetime(2013, 5, 1)
        date2 = datetime(2013, 6, 1)

        self.assertEqual(models.Project.objects.total_planned_expenditure(date1), 0)

        for i in range(5):
            project = factories.ProjectFactory()
            factories.PlanningFactory(project=project, planned_expenses=100, date=date1)
            factories.PlanningFactory(project=project, planned_expenses=200, date=date2)

        # Should include only may expenditure
        projects = models.Project.objects.all()
        total = sum([p.planned_expenditure(date1) for p in projects])
        self.assertEqual(projects.total_planned_expenditure(date1), total)

        # Should include both may and june expenditure
        total = sum([p.planned_expenditure(date2) for p in projects])
        self.assertEqual(projects.total_planned_expenditure(date2), total)

        # Check that subsets are catered for - i.e. not just .all()
        district = projects[0].municipality.district
        projects = models.Project.objects.district(district)
        total = sum([p.planned_expenditure(date1) for p in projects])
        self.assertEqual(projects.total_planned_expenditure(date1), total)
        total = sum([p.planned_expenditure(date2) for p in projects])
        self.assertEqual(projects.total_planned_expenditure(date2), total)

    def test_percentage_actual_expenditure(self):
        projects = models.Project.objects.district(self.munic1.district)
        budget = projects.total_budget()
        actual_expenditure = projects.total_actual_expenditure(self.date)
        self.assertEqual(projects.percentage_actual_expenditure(self.date), actual_expenditure / budget * 100)

        models.Project.objects.all().delete()
        project = factories.ProjectFactory()
        self.assertEqual(models.Project.objects.all().percentage_actual_expenditure(self.date), 0)

        models.Project.objects.all().delete()
        project = factories.ProjectFactory()
        factories.ProjectFinancialFactory(project=project, total_anticipated_cost=100)
        self.assertEqual(models.Project.objects.all().total_actual_expenditure(self.date), 0)
