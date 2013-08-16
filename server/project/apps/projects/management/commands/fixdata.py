from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from project.apps.projects import models

class Command(BaseCommand):
    args = ''
    help = 'Fixed data where possible - currently only ensures that ProjectCalculations are properly set. Currently idempotent but this isn''t guaranteed in future'

    def handle(self, *args, **options):
        with transaction.commit_on_success():
            for ms in models.MonthlySubmission.objects.all():
                ms.save()

            for pl in models.Planning.objects.all():
                pl.save()
