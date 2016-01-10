import iso8601
import json
import time

from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from django.db import transaction
from libs.database.database import UUID, dump_to_json
from libs.database.backend import connection

from entry.models import Project

class Command(BaseCommand):
    # args = 'filename'
    help = 'Filter project rows so we store only the last revision per month'

    def handle(self, *args, **kwargs):
        project_ids = connection.smembers('/project')

        for project_id in project_ids:
            if project_id:
                revisions = {}

                for revision_id in connection.smembers('/project/%s' % project_id):
                    updated_at = UUID(revision_id).timestamp()
                    year_month = updated_at.strftime('%Y%m')

                    if year_month not in revisions or updated_at > revisions[year_month][1]:
                        revisions[year_month] = (revision_id, updated_at)

                keepers = []
                for year_month, revision in revisions.iteritems():
                    (revision_id, updated_at) = revision
                    keepers.append(revision_id)

                for revision_id in connection.smembers('/project/%s' % project_id):
                    if revision_id not in keepers:
                        connection.sadd('/deletes', dump_to_json([ project_id, revision_id ]))
                        connection.delete('/project/%s/%s' % (project_id, revision_id))
                        connection.srem('/project/%s' % project_id, revision_id)
