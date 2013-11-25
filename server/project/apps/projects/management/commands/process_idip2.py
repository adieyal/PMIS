import sys
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from project.apps.projects import models

import _spreadsheet as spreadsheet
import _utils as utils
from _userdialogue import UserDialogue, SkipException
from parsers import ProjectSheetParser, ImplementationProjectParser

class TestDialogue(UserDialogue):
    def ask_month(self): return 10
    def ask_year(self): return 2013
    def ask_client(self): return models.Client.objects.get(name="DoE")

ud = UserDialogue()
ud = TestDialogue()

class ProjectSaver(object):
    @staticmethod
    def save_project(client, jsproject, nextstep):
        try:
            programme = ud.ask_programme(jsproject["programme"], client)
            district = ud.ask_district(jsproject["district"])
            municipality = ud.ask_municipality(jsproject["municipality"], district)
            project = ProjectSaver.find_project(jsproject, programme, district)
            ns = nextstep.nextstep(jsproject)
            if project == None:
                project = ProjectSaver.create_new_project(jsproject, programme, municipality, ns)
            ProjectSaver.save_details(project, jsproject)

        except SkipException:
            return

    @staticmethod
    def find_project(project, programme, district):
        if project["contract"] != "":
            projects = models.Project.objects.filter(project_number=project["contract"])
            if len(projects) == 0:
                pass
            elif len(projects) == 1:
                return projects[0]
            else:
                print "Multiple projects with contract number: %s" % project["contract"]
                project = ud.ask_project(project, project_number=project["contract"])
                if not project:
                    raise SkipException("Seems like multiple projects already exist")
                return project

        if project["description"] != "":
            projects = models.Project.objects.filter(name=project["description"])
            if len(projects) == 0:
                pass
            elif len(projects) == 1:
                return projects[0]
            else:
                print "Multiple projects with name: %s" % project["description"]
                project = ud.ask_project(project, name=project["description"])
                if not project:
                    raise SkipException("Seems like multiple projects already exist")
                return project
        return ud.ask_project(project, programme=programme, municipality__district=district)

    @staticmethod
    def create_new_project(project, programme, municipality, nextstep):
        return models.Project.objects.create(
            name=project["description"], project_number=project["contract"],
            programme=programme, municipality=municipality, current_step=nextstep
        )

    @staticmethod
    def save_details(project, details):
        project_financial, _ = models.ProjectFinancial.objects.get_or_create(project=project)
        project_financial.total_anticipated_cost = details["total_anticipated_cost"]
        project_financial.previous_expenses = details["total_previous_expenses"]
        project_financial.save()

        budget, _ = models.Budget.objects.get_or_create(project=project, year=details["fyear"])
        budget.allocated_budget = details["allocated_budget_for_year"]
        budget.save()

        for p in details["planning"]:
            try:
                pl = models.Planning.objects.get(date__month=p["date"].month, date__year=p["date"].year, project=project)
            except models.Planning.DoesNotExist:
                pl = models.Planning.objects.create(date=p["date"], project=project)

            pl.planned_progress = p["progress"] 
            pl.planned_expenses = p["expenditure"] 
            print p
            pl.save()
            

class NextStep(object): pass
class AlwaysPracticalCompletion(NextStep):
    def nextstep(self, project):
        return models.Milestone.practical_completion()

class Command(BaseCommand):
    args = "<filename>"
    help = "load idip file"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def process_implementation(self, sheet):
        print "Processing Implementation Sheet"
        sheet_parser = ProjectSheetParser(sheet)
        project_parser = ImplementationProjectParser(sheet, self.fyear)

        for project_range in sheet_parser.projects:
            project = project_parser.parse(project_range)
            ProjectSaver.save_project(self.client, project, AlwaysPracticalCompletion())

    def process_planning(self, sheet):
        print "Processing Planning Sheet"
        pass

    def process_retention(self, sheet):
        print "Processing Retention Sheet"
        pass

    def process_file(self, filename):
        print "Loading file ..."
        workbook = spreadsheet.WorkBook(filename)
        for sheet in workbook.sheets():
            name = sheet.name.upper()
            if "IMPLEMENTATION" in name:
                self.process_implementation(sheet)
            elif "PLANNING" in name:
                self.process_planning(sheet)
            elif "RETENTION" in name:
                self.process_retention(sheet)

    @property
    def process_details(self):
        return """
        Year: %(year)d
        Month: %(month)d
        Client: %(client)s
        Financial Year: %(fyear)d
        Financial Year Months: %(fmonths)s
        """ % self.__dict__

    def acquire_parameters(self):
        self.year = ud.ask_year()
        self.month = ud.ask_month()
        self.client = ud.ask_client()

        self.fyear = utils.fyear(self.month, self.year)
        self.fmonths = utils.fmonths(self.fyear)

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("Expected IDIP filename")

        filename = args[0]

        self.acquire_parameters()
        print self.process_details

        self.process_file(filename)

