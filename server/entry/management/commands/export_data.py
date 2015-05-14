import iso8601
import json

from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from django.db import transaction
from libs.database.database import UUID
from libs.database.backend import connection

from entry.models import Project

class Command(BaseCommand):
    # args = 'filename'
    help = 'Export project data to database'

    def translate_cluster(self, cluster):
        return cluster.lower().replace('department of ', '').replace(' ', '-').replace(',', '')

    def handle(self, *args, **kwargs):
        with transaction.commit_on_success():
            Project.objects.all().delete()

            project_ids = connection.smembers('/project')

            for project_id in project_ids:
                data = connection.get('/project/%s/edit' % (project_id))

                if data:
                    edit = json.loads(data)

                    if 'cluster' in edit:
                        cluster_id = self.translate_cluster(edit['cluster'])
                    else:
                        cluster_id = None

                    updated_at = UUID(edit['_timestamp']).timestamp()

                    print 'Creating project edit'
                    Project.objects.create(cluster_id=cluster_id, project_id=project_id, revision_id='edit', updated_at=updated_at, data=data)

                if project_id:
                    for revision_id in connection.smembers('/project/%s' % project_id):
                        data = connection.get('/project/%s/%s' % (project_id, revision_id))

                        if data:
                            revision = json.loads(data)

                            if 'cluster' in revision:
                                cluster_id = self.translate_cluster(revision['cluster'])
                            else:
                                cluster_id = None

                            updated_at = UUID(revision_id).timestamp()

                            print 'Creating project revision'
                            project = Project.objects.create(cluster_id=cluster_id, project_id=project_id, revision_id=revision_id, updated_at=updated_at, data=data)
