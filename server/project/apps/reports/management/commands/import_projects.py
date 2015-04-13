from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<cluster_id cluster_id ...>'
    help = 'Imports projects from the combined cluster *.XLS spreadsheet'

    def handle(self, *cluster_ids, **options):
        for cluster_id in cluster_ids:
            # Read the spreadsheet from the cluster_id somehow
            projects = []

            self.stdout.write('Successfully imported %s new projects from %s clusters' % (len(projects), len(cluster_ids)))
