from django.db import transaction
from .._userdialogue import SkipException
from project.apps.projects import models

class ImplementationProjectSaver(object):
    def __init__(self, userdialog):
        self.ud = userdialog

    def save_project(self, client, details):
        try:
            print details["description"]
            programme = self.ud.ask_programme(details["programme"], client)
            if not programme:
                programme = models.Programme.objects.create(name=details["programme"], client=client)
                
            district = self.ud.ask_district(details["district"])
            municipality = self.ud.ask_municipality(district, details["municipality"])
            project = self.find_project(details, programme, district)
            if project == None:
                project = self.create_new_project(details, programme, municipality)
            self.save_details(project, details)

        except SkipException:
            return

    def find_project(self, details, programme, district):
        if details["contract"] != "":
            projects = models.Project.objects.filter(project_number=details["contract"])
            if len(projects) == 0:
                pass
            elif len(projects) == 1:
                return projects[0]
            else:
                print "Multiple projects with contract number: %s" % details["contract"]
                project = self.ud.ask_project(details["description"], project_number=details["contract"])
                if not project:
                    raise SkipException("Seems like multiple projects already exist")
                return project

        if details["description"] != "":
            projects = models.Project.objects.filter(name=details["description"])
            if len(projects) == 0:
                pass
            elif len(projects) == 1:
                return projects[0]
            else:
                print "Multiple projects with name: %s" % details["description"]
                project = self.ud.ask_project(details, name=details["description"])
                if not project:
                    raise SkipException("Seems like multiple projects already exist")
                return project

        return self.ud.ask_project(proj=details["description"], programme=programme, municipality__district=district)

    def create_new_project(self, details, programme, municipality):
        return models.Project.objects.create(
            name=details["description"], project_number=details["contract"],
            programme=programme, municipality=municipality 
        )

    @transaction.commit_on_success()
    def save_details(self, project, details):
        self.save_project_financial(project, details)
        self.save_budget(project, details)
        self.save_planning(project, details)
        self.save_submissions(project, details)
        self.save_milestones(project, details)
        self.save_entities(project, details)
        self.save_next_milestone(project, details)

    def save_project_financial(self, project, details):
        project_financial, _ = models.ProjectFinancial.objects.get_or_create(project=project)

        project_financial.total_anticipated_cost = 0
        if "total_anticipated_cost" in details:
            project_financial.total_anticipated_cost = details["total_anticipated_cost"]

        project_financial.previous_expenses = 0
        if "total_previous_expenses" in details:
            project_financial.previous_expenses = details["total_previous_expenses"]

        project_financial.final_accounts = 0
        if "final_accounts" in details:
            project_financial.final_accounts = details["final_accounts"]

        project_financial.save()

    def save_budget(self, project, details):
        budget, _ = models.Budget.objects.get_or_create(project=project, year=details["fyear"])
        budget.allocated_budget = details["allocated_budget_for_year"]
        budget.save()

    def save_planning(self, project, details):
        highest_progress = 0
        for p in details["planning"]:
            try:
                pl = models.Planning.objects.get(date__month=p["date"].month, date__year=p["date"].year, project=project)
            except models.Planning.DoesNotExist:
                pl = models.Planning.objects.create(date=p["date"], project=project)
            highest_progress = max(highest_progress, p["progress"])

            pl.planned_progress = p["progress"] or highest_progress
            pl.planned_expenses = p["expenditure"] 
            pl.save()

    def save_submissions(self, project, details):
        month = self.ud.ask_month()
        year = self.ud.ask_year()
        highest_progress = 0
        for p in details["actual"]:
            try:
                ms = models.MonthlySubmission.objects.get(date__month=p["date"].month, date__year=p["date"].year, project=project)
            except models.MonthlySubmission.DoesNotExist:
                ms = models.MonthlySubmission.objects.create(date=p["date"], project=project, actual_expenditure=0, actual_progress=0)
            highest_progress = max(highest_progress, p["progress"])

            if p["date"].month == month and p["date"].year == year:
                ms.comment = details["comments"]
                ms.remedial_action = details["remedial_action"]

            ms.actual_progress = p["progress"] or highest_progress
            ms.actual_expenditure = p["expenditure"] 
            ms.save()

    def save_milestones(self, project, details):

        milestone, _ = models.ProjectMilestone.objects.get_or_create(
            project=project,
            milestone=models.Milestone.start_milestone()
        )
        milestone.completion_date = details["actual_start"] or details["planned_start"]
        milestone.save()

        milestone, _ = models.ProjectMilestone.objects.get_or_create(
            project=project,
            milestone=models.Milestone.practical_completion()
        )
        milestone.completion_date = details["actual_completion"] or details["planned_completion"]
        milestone.save()

        milestone, _ = models.ProjectMilestone.objects.get_or_create(
            project=project,
            milestone=models.Milestone.final_completion()
        )
        milestone.completion_date = details["actual_final_accounts"] or details["planned_final_accounts"]
        milestone.save()

        milestone, _ = models.ProjectMilestone.objects.get_or_create(
            project=project,
            milestone=models.Milestone.final_accounts()
        )
        milestone.completion_date = details["actual_final_accounts"] or details["planned_final_accounts"]
        milestone.save()

    def save_entities(self, project, details):
        contractor, _ = models.Role.objects.get_or_create(name="Contractor")
        consultant, _ = models.Role.objects.get_or_create(name="Consultant")
        agent, _ = models.Role.objects.get_or_create(name="Implementing Agent")

        entity, _ = models.Entity.objects.get_or_create(name=details["contractor"])
        project_role, _ = models.ProjectRole.objects.get_or_create(project=project, role=contractor)
        project_role.entity = entity
        project_role.save()

        entity, _ = models.Entity.objects.get_or_create(name=details["implementing_agent"])
        project_role, _ = models.ProjectRole.objects.get_or_create(project=project, role=agent)
        project_role.entity = entity
        project_role.save()

        entity, _ = models.Entity.objects.get_or_create(name=details["principal_agent"])
        project_role, _ = models.ProjectRole.objects.get_or_create(project=project, role=consultant)
        project_role.entity = entity
        project_role.save()

    def save_next_milestone(self, project, details):
        progress = max([a["progress"] for a in details["actual"]])
        if progress == 100:
            project.current_step = models.Milestone.final_completion()
        else:
            project.current_step = models.Milestone.practical_completion()
        project.save()

