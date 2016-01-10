import os
import re
import time
import datetime
import json as json
from optparse import make_option
from dateutil.parser import parse
from django.conf import settings
from django.utils.text import slugify
from django.core.management.base import BaseCommand, CommandError
from libs.database.database import Project, UUID
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch.client import IndicesClient
from reports.views import generate_cluster_dashboard_v2

MAX_LONG = 9223372036854775807

def make_null(project, field):
    if field in project and project[field] == '':
        project[field] = None

def safe_float(val):
    try:
        return float(filter(lambda x: x.isdigit() or x == '.', str(val)))
    except (TypeError, ValueError):
        return None
            
def translate_cluster(cluster):
    cluster = cluster or u'Unknown'
    cluster = slugify(re.sub(r'^Department of', '', cluster))
    return cluster

client = Elasticsearch()
indices_client = IndicesClient(client)

class Command(BaseCommand):
    help = 'Seed Elasticsearch indices from Redis'

    float_fields = [
        'budget_implementation',
        'budget_planning',
        'allocated_budget_for_year',
        'budget_variation_orders',
        'expenditure_in_year',
        'expenditure_to_date',
        'total_anticipated_cost',
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

    option_list = BaseCommand.option_list + (
        make_option('--recreate',
            action='store_true',
            dest='recreate',
            default=False,
            help='Recreate index'), )

    def process_entry(self, body, entry, title):
        entry['expenditure'] = safe_float(entry['expenditure'])
        entry['progress'] = safe_float(entry['progress'])

        if entry['expenditure'] is not None and (entry['expenditure'] > MAX_LONG or entry['expenditure'] < 0):
            # print '%s expenditure is suspicious (%s): %s' % (title, entry['expenditure'], body['url'])
            entry['expenditure'] = None

        if entry['progress'] is not None and (entry['progress'] > 100 or entry['progress'] < 0):
            # print '%s progress is suspicious (%s): %s' % (title, entry['progress'], body['url'])
            entry['progress'] = None

        if 'date' in entry:
            date = parse(entry['date'])

            year = date.year
            month = date.month

            if month <= 3:
                fin_year = year - 1
            else:
                fin_year = year

            financial_year = self.get_fin_year(fin_year, body)

            which = title.lower()

            if entry.get('expenditure'):
                body['calculated']['expenditure'][which] += entry['expenditure']
                financial_year['expenditure'][which] += entry['expenditure']

        else:
            pass # print 'Strange entry for %s: %s: %s' % (title, entry, body['url'])

        return dict(body)

    def get_fin_year(self, fin_year, body):
        if fin_year not in body['calculated']['financial_years']:
            body['calculated']['financial_years'][fin_year] = dict(expenditure=dict(planned_to_date=0, actual_to_date=0, planned=0, actual=0), progress=dict(planned=None, actual=None))
        return body['calculated']['financial_years'][fin_year]

    def process_progress(self, body):
        for fin_year in xrange(2013, datetime.datetime.now().year+1):
            planned = None
            actual = None

            end_year = fin_year + 1
            end_month = 3

            end = datetime.datetime(end_year, end_month, 1, 0, 0, 0)

            for entry in body.get('planning', []):
                if 'date' in entry:
                    date = parse(entry['date'])

                    if date is not None and date < end and entry['progress'] is not None and (planned is None or date > parse(planned['date'])):
                        planned = entry

            for entry in body.get('actual', []):
                if 'date' in entry:
                    date = parse(entry['date'])

                    if date is not None and date < end and entry['progress'] is not None and (actual is None or date > parse(actual['date'])):
                        actual = entry

            financial_year = self.get_fin_year(fin_year, body)

            if planned is not None:
                financial_year['progress']['planned'] = planned['progress']

            if actual is not None:
                financial_year['progress']['actual'] = actual['progress']

    def process_expenditure_totals(self, body):
        planned = 0
        actual = 0

        for fin_year in xrange(2013, datetime.datetime.now().year+1):
            financial_year = self.get_fin_year(fin_year, body)

            planned += financial_year['expenditure']['planned']
            actual += financial_year['expenditure']['actual']

            financial_year['expenditure']['planned_to_date'] = planned
            financial_year['expenditure']['actual_to_date'] = actual

    def handle(self, *args, **options):
        if options['recreate']:
            self.recreate_index()

        s = Search(client, 'pmis')
        s = s.params(search_type='count')

        s.aggs.metric('timestamp_stats', 'extended_stats', field='timestamp')

        r = s.execute()
        
        if r.aggregations.timestamp_stats['max'] is None:
            max_datetime = None
        else:
            max_datetime = datetime.datetime.utcfromtimestamp(r.aggregations.timestamp_stats['max'] / 1000)
            print 'Max timestamp: %s' % max_datetime

        base_url = os.getenv('BASE_URL', settings.BASE_URL)

        for project_id in Project.list():
            if project_id:
                revisions = Project.get_all(project_id)

                for body in revisions:
                    dt = UUID(body['_timestamp']).timestamp()

                    if max_datetime is None or dt > max_datetime:
                        body['timestamp'] = dt

                        body['project_id'] = body['_uuid']

                        # Django doesn't like _variables, don't do it
                        del(body['_uuid'])

                        body['id'] = '%s/%s' % (body['project_id'], body['timestamp'])

                        body['description'] = body.get('description')
                        body['unanalyzed_description'] = body.get('description')

                        body['name'] = body.get('name', 'NO NAME')
                        body['unanalyzed_name'] = body.get('name', 'NO NAME')

                        body['url'] = '%s/reports/project/%s/latest/' % (base_url, project_id)
                        body['edit_url'] = '%s/entry/%s/edit' % (base_url, project_id)

                        body['cluster_id'] = translate_cluster(unicode(body.get('cluster', u'')))
                        body['programme_id'] = slugify(body.get('programme', u''))

                        body['calculated'] = dict(
                            expenditure=dict(planned=0, actual=0),
                            financial_years=dict(),
                        )

                        for entry in body.get('planning', []):
                            body = self.process_entry(body, entry, 'Planned')

                        for entry in body.get('actual', []):
                            body = self.process_entry(body, entry, 'Actual')

                        self.process_expenditure_totals(body)
                        self.process_progress(body)

                        for field in self.float_fields:
                            body[field] = safe_float(body.get(field))

                        for field in self.date_fields:
                            if body.get(field, None) == '':
                                body[field] = None

                        client.index(index='pmis', doc_type='project', id=body['id'], body=body)

    def recreate_index(self):
        if indices_client.exists(index='pmis'):
            indices_client.delete(index='pmis')

        body = {
            'mappings': {
                'project': {
                    'properties': {
                        "municipality" : {
                            "type" : "string"
                        },
                        "expenditure_percent_of_budget" : {
                            "type" : "double"
                        },
                        "fyear" : {
                            "type" : "long"
                        },
                        "contract_award_date" : {
                            "type" : "date",
                            "format" : "dateOptionalTime"
                        },
                        "source" : {
                            "type" : "string"
                        },
                        "planning_start" : {
                            "format" : "dateOptionalTime",
                            "type" : "date"
                        },
                        "phase" : {
                            "type" : "string"
                        },
                        "budget_implementation" : {
                            "type" : "long"
                        },
                        "total_previous_expenses" : {
                            "type" : "string"
                        },
                        "remedial_action" : {
                            "type" : "string"
                        },
                        "contractor" : {
                            "type" : "string"
                        },
                        "contract" : {
                            "type" : "string"
                        },
                        "last_modified_user" : {
                            "type" : "string"
                        },
                        "district" : {
                            "type" : "string"
                        },
                        "remedial_action_previous" : {
                            "type" : "string"
                        },
                        "location" : {
                            "type" : "string"
                        },
                        "cluster_id" : {
                            "type" : "string"
                        },
                        "budget_planning" : {
                            "type" : "long"
                        },
                        "final_account" : {
                            "type" : "double"
                        },
                        "implementation_handover" : {
                            "format" : "dateOptionalTime",
                            "type" : "date"
                        },
                        "planning_completion" : {
                            "type" : "date",
                            "format" : "dateOptionalTime"
                        },
                        "jobs" : {
                            "type" : "string"
                        },
                        "total_confirmed_budget" : {
                            "type" : "long"
                        },
                        "allocated_budget_for_year" : {
                            "type" : "long"
                        },
                        "actual_start" : {
                            "format" : "dateOptionalTime",
                            "type" : "date"
                        },
                        "planning_phase" : {
                            "type" : "string"
                        },
                        "expenditure_to_date" : {
                            "type" : "long"
                        },
                        "actual_final_accounts" : {
                            "format" : "dateOptionalTime",
                            "type" : "date"
                        },
                        "planning" : {
                            "properties" : {
                                "date" : {
                                    "format" : "dateOptionalTime",
                                    "type" : "date"
                                },
                                "expenditure" : {
                                    "type" : "long"
                                },
                                "progress" : {
                                    "type" : "short"
                                }
                            }
                        },
                        "comments_previous" : {
                            "type" : "string"
                        },
                        "planned_final_accounts" : {
                            "type" : "date",
                            "format" : "dateOptionalTime"
                        },
                        "implementing_agent" : {
                            "type" : "string"
                        },
                        "actual" : {
                            "properties" : {
                                "date" : {
                                    "format" : "dateOptionalTime",
                                    "type" : "date"
                                },
                                "expenditure" : {
                                    "type" : "long"
                                },
                                "progress" : {
                                    "type" : "short"
                                }
                            }
                        },
                        "budget_variation_orders" : {
                            "type" : "long"
                        },
                        "title" : {
                            "type" : "string"
                        },
                        "unanalyzed_description" : {
                            "type" : "string",
                            "index": "not_analyzed"
                        },
                        "principal_agent" : {
                            "type" : "string"
                        },
                        "programme" : {
                            "type" : "string"
                        },
                        "circuit" : {
                            "type" : "string"
                        },
                        "timestamp" : {
                            "format" : "dateOptionalTime",
                            "type" : "date"
                        },
                        "planned_start" : {
                            "type" : "date",
                            "format" : "dateOptionalTime"
                        },
                        "name" : {
                            "type" : "string"
                        },
                        "unanalyzed_name" : {
                            "type" : "string",
                            "index" : "not_analyzed"
                        },
                        "comments" : {
                            "type" : "string"
                        },
                        "expenditure_in_year" : {
                            "type" : "long"
                        },
                        "last_modified_time" : {
                            "type" : "date",
                            "format" : "dateOptionalTime"
                        },
                        "total_anticipated_cost" : {
                            "type" : "long"
                        },
                        "url" : {
                            "type" : "string"
                        },
                        "actual_completion" : {
                            "format" : "dateOptionalTime",
                            "type" : "date"
                        },
                        "id" : {
                            "index": "not_analyzed",
                            "type" : "string"
                        },
                        "_uuid" : {
                            "index": "not_analyzed",
                            "type" : "string"
                        },
                        "total_anticipated_in_year" : {
                            "type" : "double"
                        },
                        "extensions" : {
                            "type" : "string"
                        },
                        "cluster" : {
                            "type" : "string",
                            "index": "not_analyzed"
                        },
                        "scope" : {
                            "type" : "string"
                        },
                        "manager" : {
                            "type" : "string"
                        },
                        "state" : {
                            "type" : "string"
                        },
                        "revised_completion" : {
                            "type" : "date",
                            "format" : "dateOptionalTime"
                        },
                        "description" : {
                            "type" : "string"
                        },
                        "planned_completion" : {
                            "type" : "date",
                            "format" : "dateOptionalTime"
                        },
                        "programme_id" : {
                            "type" : "string"
                        }
                    }
                }
            }
        }

        indices_client.create(index='pmis', body=body)
