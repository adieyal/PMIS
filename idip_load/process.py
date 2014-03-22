import sys
import json
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

#from project.apps.projects import models

import _spreadsheet as spreadsheet
import _utils as utils
#from _userdialogue import UserDialogue, SkipException
import parsers
import savers

class TestDialogue(object):#UserDialogue):
    def ask_month(self): return 12
    def ask_year(self): return 2013
    def ask_client(self): return 'DoE'

#ud = UserDialogue()
ud = TestDialogue()

class Command(object):
    args = "<filename>"
    help = "load idip file"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def process_implementation(self, sheet):
        print "Processing Implementation Sheet"
        sheet_parser = parsers.ImplementationProjectSheetParser(sheet)
        project_parser = parsers.ImplementationProjectParser(sheet, self.fyear)
        saver = savers.ProjectSaver(ud)

        for project_range in sheet_parser.projects:
            project = project_parser.parse(project_range)
            #print utils.dump_to_json(project)
            saver.save_project(self.client, project)

    def process_planning(self, sheet):
        print "Processing Planning Sheet"
        sheet_parser = parsers.PlanningProjectSheetParser(sheet)
        project_parser = parsers.PlanningProjectParser(sheet, self.fyear)
        #saver = savers.PlanningProjectSaver(ud)
        saver = savers.ProjectSaver(ud)

        for project_range in sheet_parser.projects:
            project = project_parser.parse(project_range)
            saver.save_project(self.client, project)

    def process_retention(self, sheet):
        print "Processing Retention Sheet"
        sheet_parser = parsers.RetentionProjectSheetParser(sheet)
        project_parser = parsers.RetentionProjectParser(sheet, self.month, self.fyear)
        #saver = savers.RetentionProjectSaver(ud)
        saver = savers.ProjectSaver(ud)

        for project_range in sheet_parser.projects:
            project = project_parser.parse(project_range)
            saver.save_project(self.client, project)

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

if __name__=='__main__':
    c = Command()
    c.handle(sys.argv[1])
