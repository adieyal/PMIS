from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from project.apps.projects import models

class Command(BaseCommand):
    args = ''
    help = 'Fixed data where possible - currently only ensures that ProjectCalculations are properly set. Currently idempotent but this isn''t guaranteed in future'

    def calculate_bad_projects(self):
        print "Running through all submissions"
        for ms in models.MonthlySubmission.objects.all():
            ms.save()

        print "Running through all planning objects"
        for pl in models.Planning.objects.all():
            pl.save()

    def handle(self, *args, **options):
        with transaction.commit_on_success():
            self.calculate_bad_projects()
