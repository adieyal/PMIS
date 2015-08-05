import re

from django.core.management.base import BaseCommand, CommandError

from datetime import datetime
from libs.database.database import Project
from entry.models import Municipality
from titlecase import titlecase
from Levenshtein import distance

def title_case(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])

class Command(BaseCommand):
    args = ''
    help = 'Fix projects by changing data forcibly'

    def handle(self, *args, **options):
        municipalities = Municipality.objects.values_list('name', flat=True)

        project_ids = Project.list()
        for project_id in project_ids:
            project = Project.get(project_id)

            if project.municipality not in municipalities:
                if project.municipality is not None:
                    # Strip off brackets
                    project.municipality = re.sub(r"\(.*\)$", "", project.municipality).strip()

                    if project.municipality:
                        municipality = None
                        shortest_distance = None

                        for m in municipalities:
                            d = distance(project.municipality, m)
                            if shortest_distance is None or d < shortest_distance:
                                shortest_distance = d
                                municipality = m

                        if shortest_distance < len(project.municipality) - 2 and shortest_distance < len(municipality) - 2 and shortest_distance < 10:
                            print "Renaming %s to %s" % (project.municipality, municipality)

                            project._details['municipality'] = municipality
                            project.save(False)
