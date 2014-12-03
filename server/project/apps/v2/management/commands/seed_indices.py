import json as json
from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError
from project.libs.database.database import Project
from elasticsearch import Elasticsearch
from project.apps.reports.views import generate_cluster_dashboard_v2

def make_null(project, field):
    if field in project and project[field] == '':
        project[field] = None

es = Elasticsearch()

class Command(BaseCommand):
    help = 'Seed Elasticsearch indices from Redis'

    clusters = [
        "education",
        "health",
        "social-development",
        "culture-sports-science-and-recreation",
        "community-safety-security-and-liaison",
        "economic-development-environment-and-tourism",
    ]

    date_fields = [
        'planning_completion',
        'planned_completion',
        'planning_start',
        'planned_start',
        'actual_start',
        'actual_completion',
        'implementation_handover',
        'revised_completion',
    ]

    def handle(self, *args, **options):
        for c in self.clusters:
            cluster = generate_cluster_dashboard_v2('department-of-%s' % c)
            
            for programme in cluster['programmes']:
                if programme['title']:
                    programme_id = '%s:%s' % (c, slugify(unicode(programme['title'])))

                    body = {
                        'id': 'programme:%s' % programme_id,
                        'title': programme['title'],
                        'cluster': cluster['client'],
                        'cluster_id': c,
                    }

                    es.index(index='pmis', doc_type='programme', id=programme_id, body=body)

            for project_id in Project.list():
                if project_id:
                    project = Project.get(project_id, True)
                    body = {
                        'id': 'project:%s' % project_id,
                        'title': project['description'],

                        # Probably need to do this correctly :)
                        'url': 'http://www.backend.dev/reports/project/%s/latest/' % project_id,

                        'cluster': cluster['client'],
                        'cluster_id': c,
                        'manager': project.get('manager'),
                        'municipality': project.get('municipality'),
                        'comments': project.get('comments'),
                        'programme': project.get('programme'),
                        'programme_id': slugify(project.get('programme', u'')),
                    }
                    es.index(index='pmis', doc_type='project', id=project_id, body=body)
