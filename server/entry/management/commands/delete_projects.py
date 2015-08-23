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
            try:
                project = Project.get(uuid)
                name = project.name
                project.clear()
                print 'Deleted project %s' % name
            except Exception, e:
                print e
                pass
