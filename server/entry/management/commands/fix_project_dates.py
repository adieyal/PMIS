import iso8601
from django.core.management.base import BaseCommand, CommandError

from datetime import datetime
from libs.database.database import Project


class Command(BaseCommand):
    args = ''
    help = 'Fix project dates for month-based fields'

    def find_or_add_month(self, data, year, month):
        for entry in data:
            d = iso8601.parse_date(entry['date'])

            if d.year == year and d.month == month:
                return

        data.append({
            'expenditure': None,
            'progress': None,
            'date': '%04d-%02d-01T00:00:00' % (year, month)
        })

    def handle(self, *args, **options):
        projects = Project.list()

        this_year = datetime.now().year

        for uuid in projects:
            project = Project.get(uuid)

            for current_year in xrange(2013, this_year + 2):
                if (current_year == 2013):
                    start = 4
                else:
                    start = 1

                if (current_year == this_year + 1):
                    stop = 4
                else:
                    stop = 13

                for current_month in xrange(start, stop):
                    print 'Checking %s-%s' % (current_year, current_month)

                    self.find_or_add_month(project.actual, current_year, current_month)
                    self.find_or_add_month(project.planning, current_year, current_month)

            project._details['actual'] = sorted(project.actual, key=lambda x: x['date'])
            project._details['planning'] = sorted(project.planning, key=lambda x: x['date'])

            project.edit = False
            project._details['last_modified_time'] = datetime.now().isoformat()

            project.save()
