from dateutil.parser import parse
import datetime
import time

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

def projects_by_fin_year(fin_year, exclude_previous=True):
    gte = datetime.datetime(fin_year, 4, 1, 0, 0, 0)
    lt = datetime.datetime(fin_year + 1, 4, 1, 0, 0, 0)

    search = Search(using=client, index='pmis') \
        .filter('range', timestamp={ 'lt': lt })

    if exclude_previous:
        search = search.filter('range', timestamp={ 'gte': gte, 'lt': lt })

    search.aggs \
        .bucket('projects', 'terms', field='_uuid', size=0) \
        .bucket('revisions', 'terms', field='id', order={ '_term': 'desc' }, size=1)

    tic = time.time()

    response = search.execute()

    keys = []

    for project in response.aggregations.projects.buckets:
        for revision in project['revisions']['buckets']:
            keys.append(revision['key'])

    toc = time.time()

    print 'Found %d project revisions in %s milliseconds' % (len(keys), (toc - tic) * 1000)

    # Now start another ES query which works the most-up-to-date project revisions only
    search = Search(using=client, index='pmis') \
        .filter('terms', id=keys)

    # Do other things with projects here
    search.aggs.metric('actual_progress', 'stats', field='calculated.financial_years.2015.progress.actual')
    search.aggs.metric('planned_progress', 'stats', field='calculated.financial_years.2015.progress.planned')

    response = search.execute()

    return response

    all = []
    old = []

    response = search.scan()

    try:
        while 1:
            hit = response.next()

            timestamp = parse(hit['timestamp'])

            if timestamp < gte:
                old.append(hit)

            all.append(hit)

            response.next()
    except StopIteration:
        pass

    print '%s old, %s total' % (len(old), len(all))

projects_by_fin_year(2015)
