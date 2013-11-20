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

        except SkipException:
            return

    @staticmethod
    def find_project(project, programme, district):
        if project["contract"] != "":
            try:
                return models.Project.objects.get(project_number=project["contract"])
            except models.Project.DoesNotExist:
                pass
            except models.Project.MultipleObjectsReturned:
                print "Multiple projects with contract number: %s" % project["contract"]
                raise SkipException("Seems like multiple projects already exist")

        if project["description"] != "":
            try:
                return models.Project.objects.get(name=project["description"])
            except models.Project.DoesNotExist:
                pass
            except models.Project.MultipleObjectsReturned:
                print "Multiple projects with the same name: %s" % project["description"]
                raise SkipException("Seems like multiple projects already exist")
        return ud.ask_project(project, programme, district)

    @staticmethod
    def create_new_project(project, programme, municipality, nextstep):
        return models.Project.objects.create(
            name=project["description"], project_number=project["contract"],
            programme=programme, municipality=municipality, current_step=nextstep
        )

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
        project_parser = ImplementationProjectParser(sheet)

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

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError("Expected IDIP filename")

        filename = args[0]

        self.year = ud.ask_year()
        self.month = ud.ask_month()
        self.client = ud.ask_client()

        self.fyear = utils.fyear(self.month, self.year)
        self.fmonths = utils.fmonths(self.fyear)

        print """
        Year: %(year)d
        Month: %(month)d
        Client: %(client)s
        Financial Year: %(fyear)d
        Financial Year Months: %(fmonths)s
        """ % self.__dict__

        self.process_file(filename)

