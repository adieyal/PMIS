from django.core.management.base import BaseCommand, CommandError

from datetime import datetime
from libs.database.database import Project
from entry.models import Municipality


class Command(BaseCommand):
    args = ''
    help = 'Validate project'

    def handle(self, *args, **options):
        municipalities = map(lambda m: m['name'], Municipality.objects.values('name'))

        project_ids = Project.list()
        for project_id in project_ids:
            project = Project.get(project_id)

            if project.municipality not in municipalities:
                print "Unknown municipality: %s" % project.municipality
