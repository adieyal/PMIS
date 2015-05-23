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

    def translate_cluster(self, project):
        if 'cluster' in project:
            return project['cluster'].lower().replace('department of ', '').replace(' ', '-').replace(',', '')
        else:
            return None

    def handle(self, *args, **kwargs):
        with transaction.commit_on_success():
            Project.objects.all().delete()

            project_ids = connection.smembers('/project')

            for project_id in project_ids:
                if project_id:
                    data = connection.get('/project/%s/edit' % (project_id))

                    if data:
                        revision = json.loads(data)
                        cluster_id = self.translate_cluster(project)
                        updated_at = UUID(project['_timestamp']).timestamp()

                        print 'Creating project edit'
                        project = Project.objects.get_or_create(cluster_id=cluster_id, project_id=project_id)

                        project.revision_set.create(
                            revision_id='edit',
                            updated_at=updated_at,
                            data=data
                        )

                    for revision_id in connection.smembers('/project/%s' % project_id):
                        data = connection.get('/project/%s/%s' % (project_id, revision_id))

                        if data:
                            revision = json.loads(data)
                            cluster_id = self.translate_cluster(project)
                            updated_at = UUID(revision_id).timestamp()

                            print 'Creating project revision'
                            project = Project.objects.get_or_create(cluster_id=cluster_id, project_id=project_id)

                            project.revision_set.create(
                                revision_id=revision_id,
                                updated_at=updated_at,
                                data=data
                            )
