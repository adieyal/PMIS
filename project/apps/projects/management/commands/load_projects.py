from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import json
from project.apps.projects import models

programme_map = {
    "MUD SCHOOLS/UNSAFE/CONVENTIONAL (ON-GOING)" : "Mud and Unsafe Structures (Conventional)",
    "MUD SCHOOLS/UNSAFE/CONVENTIONAL (COMPLETED)" : "Mud and Unsafe Structures (Conventional)",
    "MUD  SCHOOLS (UNCONVENTIONAL) (ON-GOING)" : "Mud Schools (Unconventional)",
    "MUD SCHOOLS (UNCONVECTIONAL TO CONVENTIONAL)  (ON-GOING)" : "Mud Schools (Unconventional to Conventional)",
    "MUD SCHOOLS (UNCONVECTIONAL TO CONVENTIONAL) (ON-GOING)" : "Mud Schools (Unconventional to Conventional)",
    "GRADE-R SCHOOL (ON-GOING)" : "Grade R",
    "GRADE R SCHOOL (COMPLETED)" : "Grade R",
    "SUBSTITUTE SCHOOLS (ON-GOING)" : "Substitute Schools",
    "SUBSTITUTE SCHOOLS  (COMPLETED)" : "Substitute Schools",
    "SPECIAL SCHOOL (ON-GOING)" : "Special Schools",
    "SPECIAL SCHOOL (COMPLETED)" : "Special Schools",
    "STORM DAMAGED SCHOOLS (ON-GOING)" : "Storm Damage",
    "STORM DAMAGED SCHOOLS  (COMPLETED)" : "Storm Damage",
    "MAINTENANCE SCHOOLS (ON-GOING)" : "Maintenance",
    "MAINTENANCE SCHOOLS  (COMPLETED)" : "Maintenance",
    "CURRENT PROGRAMME (COMPLETED)" : "Current",
    "IDT MUD SCHOOLS (COMPLETED)" : "IDT Mud Schools",
    "TECHNICAL SCHOOL (ON-GOING)" : "Technical Schools",
    "TECHNICAL SCHOOL (COMPLETED)" : "Technical Schools",
    "BOARDING SCHOOL (COMPLETED)" : "Boarding Schools",
    "INTERVENTION PROGRAMME (COMPLETED)" : "Intervention",
    "SINGITA PROGRAMME (ON-GOING)" : "Singita",
    "SINGITA PROGRAMME (COMPLETED)" : "Singita",
}

district_map = {
    "nkangala" : "Nkangala",
    "ehlanzeni" : "Ehlanzeni",
    "gert sibande" : "Gert Sibande",
    "gert" : "Gert Sibande",
}

class Command(BaseCommand):
    args = 'project json file'
    help = 'Loads projects from a json file'

    def handle(self, *args, **options):
        # Ensure that unknown municipalities are created
        for district in models.District.objects.all():
            municipality = models.Municipality.objects.get_or_create(
                name="Unknown", district=district)

        data = json.load(open(args[0]))
        with transaction.commit_on_success():
            for datum in data:
                programme = programme_map[datum["programme"]]
                programme = models.Programme.objects.get(name=programme)
                try:
                    district = district_map[datum["district"].lower()]
                except KeyError:
                    # If there is an invalid district
                    #import traceback
                    #traceback.print_exc() 
                    continue
                municipality = models.Municipality.objects.get(
                    name="Unknown",
                    district__name=district
                )
                project = models.Project.objects.get_or_create(
                    name=datum["project"], programme=programme,
                    municipality=municipality
                )
