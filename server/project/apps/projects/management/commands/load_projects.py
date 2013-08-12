from django.core.management.base import BaseCommand, CommandError
from dateutil import parser as dateparser
from datetime import datetime
from django.db import transaction
import json
from project.apps.projects import models

municipalities = {
    "pixley ka seme" : "Pixley Ka Seme",
    "Pixley Ka Seme Local Municipality" : "Pixley Ka Seme",
    "Delmas Local Municipality" : "Delmas",
    "Mbombela Local Municipality" : "Mbombela",
    "Msukaligwa Local Municipality" : "Msukaligwa",
}
programme_map = {
    "MUD SCHOOLS/UNSAFE/CONVENTIONAL (ON-GOING)" : "Mud and Unsafe Structures (Conventional)",
    "MUD SCHOOLS/UNSAFE/CONVENTIONAL (COMPLETED)" : "Mud and Unsafe Structures (Conventional)",
    "MUD AND UNSAFE STRUCTURES/CONVENTIONAL (ON-GOING)" : "Mud Schools",

    "MUD  SCHOOLS (UNCONVENTIONAL) (ON-GOING)" : "Mud Schools (Unconventional)",
    "MUD  AND UNSAFE STRUCTURES (UNCONVENTIONAL) (ON-GOING)" : "Mud Schools (Unconventional)",

    "MUD SCHOOLS (UNCONVECTIONAL TO CONVENTIONAL)  (ON-GOING)" : "Mud Schools (Unconventional to Conventional)",
    "MUD SCHOOLS (UNCONVECTIONAL TO CONVENTIONAL) (ON-GOING)" : "Mud Schools (Unconventional to Conventional)",
    "MUD AND UNSAFE STRUCTURES (UNCONVECTIONAL TO CONVENTIONAL)  IDT (ON-GOING)" : "Mud Schools (Unconventional to Conventional)",

    "GRADE-R SCHOOL (ON-GOING)" : "Grade R",
    "GRADE R SCHOOL (COMPLETED)" : "Grade R",

    "SUBSTITUTE SCHOOLS (ON-GOING)" : "Substitute Schools",
    "SUBSTITUTE SCHOOLS  (COMPLETED)" : "Substitute Schools",

    "SPECIAL SCHOOL (ON-GOING)" : "Special Schools",
    "SPECIAL SCHOOL (COMPLETED)" : "Special Schools",
    "SPECIAL SCHOOLS (ON-GOING)" : "Special Schools",

    "STORM DAMAGED SCHOOLS (ON-GOING)" : "Storm Damage",
    "STORM DAMAGED SCHOOLS  (COMPLETED)" : "Storm Damage",

    "MAINTENANCE SCHOOLS (ON-GOING)" : "Maintenance",
    "MAINTENANCE SCHOOLS  (COMPLETED)" : "Maintenance",
    "DOE MAINTENANCE SCHOOLS (ONGOING)" : "Maintenance",
    "MAINTENANCE SCHOOLS (ONGOING)" : "Maintenance",

    "CURRENT PROGRAMME (COMPLETED)" : "Current",
    "CURRENT PROGRAMME (ON-GOING)" : "Current",

    "IDT MUD SCHOOLS (COMPLETED)" : "IDT Mud Schools",
    "TECHNICAL SCHOOL (ON-GOING)" : "Technical Schools",
    "TECHNICAL SCHOOL (COMPLETED)" : "Technical Schools",

    "BOARDING SCHOOL (COMPLETED)" : "Boarding Schools",
    "BOARDING SCHOOL (ON-GOING)" : "Boarding Schools",

    "INTERVENTION PROGRAMME (COMPLETED)" : "Intervention",
    "SINGITA PROGRAMME (ON-GOING)" : "Singita",
    "SINGITA PROGRAMME (COMPLETED)" : "Singita",

    "NEW SCHOOLS ( ON - GOING)" : "New Schools",

    "REFURBRISHMENT AND RENOVATION (ON-GOING)" : "Refurbishment and Renovation", 

    "ENVIROLOO SANITATION SYSTEM (ON-GOING)" : "Enviroloo Toilet",

    "EQUITABLE SHARE" : "Equitable Share",
}

district_map = {
    "nkangala" : "Nkangala",
    "ehlanzeni" : "Ehlanzeni",
    "gert sibande" : "Gert Sibande",
    "gert" : "Gert Sibande",
}

start_milestone = models.Milestone.objects.get(name="Project Identification")
practical_completion_milestone = models.Milestone.objects.get(name="Practical Completion")
final_completion_milestone = models.Milestone.objects.get(name="Final Completion")
final_accounts_milestone = models.Milestone.objects.get(name="Final Accounts")

contractor_role = models.Role.objects.get(name="Contractor")
consultant_role = models.Role.objects.get(name="Consultant")

class Command(BaseCommand):
    args = 'project json file'
    help = 'Loads projects from a json file'

    def resolve_programme(self, client, programme):
        programme =  programme_map[programme]
        programme = models.Programme.objects.get(client=client, name=programme)
        return programme

    def resolve_municipality(self, district, municipality):
        try:
            if municipality:
                municipality = municipalities[municipality]
                return models.Municipality.objects.get(name=municipality)
        except models.Municipality.DoesNotExist:
            if district:
                return models.Municipality.objects.get(
                    name="Unknown",
                    district__name=district
                )
            else:
                return models.Municipality.objects.get(
                    name="Unknown",
                    district__name="Unknown"
                )

    def create_project(self, name, programme, municipality, project_number):
        project, _ = models.Project.objects.get_or_create(
            name=name, programme=programme,
            municipality=municipality,
            project_number=project_number
        )

        return project

    def create_project_financial(self, project, total_anticipated_cost, previous_expenses):
        try:
            financial = models.ProjectFinancial.objects.get(project=project)
        except models.ProjectFinancial.DoesNotExist:
            financial, _ = models.ProjectFinancial.objects.get_or_create(
                project=project,
                previous_expenses=previous_expenses
            )

        financial.total_anticipated_cost = total_anticipated_cost
        financial.previous_expenses = previous_expenses
        financial.save()
        return financial

    def create_budget(self, project, year, total_budget, planning_budget):
        budget, _ = models.Budget.objects.get_or_create(
            year=year,
            project=project
        )
        budget.allocated_budget = total_budget
        budget.allocated_planning_budget = planning_budget
        budget.save()

        return budget

    
    def create_milestone(self, project, milestone, date):
        milestone, _ = models.ProjectMilestone.objects.get_or_create(
            project=project,
            milestone=milestone
        )
        milestone.completion_date = date
        milestone.save()
        return milestone

    def create_start_date(self, project, start_date):
        return self.create_milestone(project, start_milestone, start_date)

    def create_completion_dates(self, project, completion_dates):
        if len(completion_dates) == 3:
            self.create_milestone(project, practical_completion_milestone, completion_dates[0])
            self.create_milestone(project, final_completion_milestone, completion_dates[1])
            self.create_milestone(project, final_accounts_milestone, completion_dates[2])

    def create_planning(self, project, year, month, planned_expenses, planned_progress):
            try:
                planning = models.Planning.objects.get(
                    project=project, date=datetime(year, month, 1)
                )
            except models.Planning.DoesNotExist:
                planning = models.Planning(project=project, date=datetime(year, month, 1))

            planning.planned_expenses = planned_expenses
            planning.planned_progress = planned_progress
            planning.save()
            return planning

    def create_monthly_submission(self, project, year, month, actual_expenses, actual_progress, comment, comment_type, remedial_action):
            try:
                submission = models.MonthlySubmission.objects.get(
                    project=project, date=datetime(year, month, 1)
                )
            except models.MonthlySubmission.DoesNotExist:
                submission = models.MonthlySubmission(project=project, date=datetime(year, month, 1))

            submission.actual_expenditure=actual_expenses
            submission.actual_progress=actual_progress
            submission.comment = comment
            submission.remedial_action = remedial_action
            submission.save()
            return submission

    def set_role(self, project, role, entity_name):
        entity, _ = models.Entity.objects.get_or_create(name=entity_name)
            
        projectrole, _ = models.ProjectRole.objects.get_or_create(
            project=project, role=role, entity=entity
        )
        return projectrole

    def set_consultant(self, project, entity_name):
        return self.set_role(project, consultant_role, entity_name)

    def set_contractor(self, project, entity_name):
        return self.set_role(project, contractor_role, entity_name)

    def handle(self, *args, **options):
        # Ensure that unknown municipalities are created
        # TODO - add this to the initial_data fixture
        for district in models.District.objects.all():
            municipality = models.Municipality.objects.get_or_create(
                name="Unknown", district=district)

        client = models.Client.objects.get(name=args[1])
        data = json.load(open(args[0]))
        with transaction.commit_on_success():
            for datum in data:
                year = int(datum["year"])
                programme = self.resolve_programme(client, datum["programme"])
                municipality = self.resolve_municipality(district, datum["municipality"])

                project = self.create_project(datum["project"], programme, municipality, datum["project_code"])

                self.create_project_financial(project, float(datum["total_anticipated_cost"]), float(datum["prev_year_expenditure"]))
                self.create_budget(project, year, float(datum["allocated_budget"]), 0)
                if datum["start_date"]:
                    self.create_start_date(project, dateparser.parse(datum["start_date"]))
                self.create_completion_dates(project, map(dateparser.parse, datum["revised_completion_dates"]))

                months = zip([year - 1] * 9 + [year] * 3, models.financial_year)
                for progress in datum["progress"]:
                    self.create_planning(
                        project, progress["year"], progress["month"],
                        progress["planned_expenditure"], progress["planned_progress"]
                    )
                    if progress["year"] == datum["year"] and progress["month"] == datum["month"]:
                        comment = datum["comment"]
                        mitigation = datum["mitigation"]
                    else:
                        comment = mitigation = ""
                    comment_type = None

                    self.create_monthly_submission(
                        project, progress["year"], progress["month"],
                        progress["actual_expenditure"], progress["actual_progress"],
                        comment, comment_type, mitigation
                    )

                self.set_contractor(project, datum["contractor"])
                self.set_consultant(project, datum["consultant"])


