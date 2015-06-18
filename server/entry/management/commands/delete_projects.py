from django.core.management.base import BaseCommand, CommandError

import xlrd
from uuid import uuid4
from datetime import datetime
from scripts.spreadsheet import Spreadsheet
from libs.database.database import Project


class Command(BaseCommand):
    args = 'project_uuid [project_uuid ...]'
    help = 'Delete projects given a list of UUIDs'

    def handle(self, *args, **options):
        for uuid in args:
            project = Project.get(uuid)
            print 'Deleted project %s' % project.name
            project.clear()
