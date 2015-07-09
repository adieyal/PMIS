from django.core.management.base import BaseCommand, CommandError

from datetime import datetime
from libs.database.database import Project


class Command(BaseCommand):
    args = ''
    help = 'Iterate over projects, doing something'

    def handle(self, *args, **options):
        for uuid in args:
            project = Project.get(uuid)
