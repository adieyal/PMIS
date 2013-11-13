import sys
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from project.apps.projects import models

import _spreadsheet as spreadsheet
import _utils as utils
from _userdialogue import UserDialogue
from parsers import ProjectSheetParser

class TestDialogue(UserDialogue):
    def ask_month(self): return 10
    def ask_year(self): return 2014
    def ask_client(self): return models.Client.objects.get(name="DoE")

class Command(BaseCommand):
    args = "<filename>"
    help = "load idip file"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.ud = UserDialogue()
        self.ud = TestDialogue()

    def process_implementation(self, sheet):
        print "Processing Implementation Sheet"
        sheet_parser = ProjectSheetParser(sheet)

        for project_range in sheet_parser.projects:
            print project_range

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

        self.year = self.ud.ask_year()
        self.month = self.ud.ask_month()
        self.client = self.ud.ask_client()

        self.fyear = utils.fyear(self.month, self.year)
        self.fmonths = utils.fmonths(self.fyear)

        self.process_file(filename)

