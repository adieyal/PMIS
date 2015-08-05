import re
import json as json
import iso8601
import string
import time
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from libs.database.database import Project

from forms import IndexForm, NewIndexForm
from models import Cluster, Programme, ImplementingAgent, Municipality

client = Elasticsearch()

def _safe_int(val, add=0):
    try:
        return int(filter(lambda x: x.isdigit() or x == '.', str(val))) + add
    except (TypeError, ValueError):
        return None

def create_filter(cluster_id, query):
    def _filter(x):
        result = True

        if cluster_id:
            cluster = Cluster.objects.get(id=cluster_id)
            result = x.cluster == cluster.name

        if result:
            if query:
                lower = query.lower()
                result = lower in x.name.lower() or lower in x.contract.lower()

        return result
    return _filter

def filter_projects(request):
    cluster_id = request.GET.get('cluster')
    query = request.GET.get('query')

    projects = filter(
        create_filter(cluster_id, query),
        [Project.get(p) for p in Project.list() if p]
    )

    return projects

def search_by_fin_year(request):
    """ Create an Elasticsearch Search object which is prefiltered to the financial year """
    fin_year = int(request.GET.get('fin_year', '2015'))

    range_filter = { 'lt': datetime(fin_year + 1, 4, 1, 0, 0, 0) }

    exclude_previous = request.GET.get('exclude_previous') == 'on'

    # Exclude previous financial years' data
    if exclude_previous:
        range_filter['gte'] = datetime(fin_year, 4, 1, 0, 0, 0)

    search = Search(using=client, index='pmis') \
        .filter('range', timestamp=range_filter)

    search.aggs \
        .bucket('projects', 'terms', field='project_id', size=0) \
        .bucket('revisions', 'terms', field='id', order={ '_term': 'desc' }, size=1)

    search = search.params(search_type='count')

    response = search.execute()

    latest_ids = []

    for project in response.aggregations.projects.buckets:
        for revision in project['revisions']['buckets']:
            latest_ids.append(revision['key'])

    # Now start another ES query which works with the most-up-to-date
    # project revisions only
    search = Search(using=client, index='pmis') \
        .filter('terms', id=latest_ids)

    return search

def projects_by_fin_year(request):
    search = search_by_fin_year(request)
    total = search.params(search_type='count').execute().hits.total

    cluster_id = request.GET.get('cluster')

    if cluster_id:
        cluster = Cluster.objects.get(id=cluster_id)
        search = search.filter('term', cluster=cluster.name)

    query = request.GET.get('search[value]')

    if query:
        search = search.query('query_string', query=query)

    start = int(request.GET.get('start', '0'))
    length = int(request.GET.get('length', '10'))

    # Order
    order_column = request.GET.get('order[0][column]')
    if order_column:
        name = request.GET.get('columns[%d][data]' % int(order_column))
        name = translate_order(request, name)

        direction = request.GET.get('order[0][dir]')

        search = search.sort({ name : direction })

    # Pagination
    search = search[start:(start + length)]

    # Do other things with projects here
    # search.aggs.metric('actual_progress', 'stats', field='calculated.financial_years.2015.progress.actual')
    # search.aggs.metric('planned_progress', 'stats', field='calculated.financial_years.2015.progress.planned')

    response = search.execute()

    return (response, total)

def translate_order(request, order):
    fin_year = str(request.GET.get('fin_year', 2015))

    orders = {
        'cluster': 'cluster',
        'name': 'unanalyzed_name',
        'entered_budget': 'total_anticipated_cost',
        'calculated_budget': 'calculated.financial_years.%s.expenditure.planned_to_date' % fin_year,
        'entered_expenditure': 'expenditure_to_date',
        'calculated_expenditure': 'calculated.financial_years.%s.expenditure.actual_to_date' % fin_year
    }
    return orders[order]

def create_map(request):
    def _map(project):
        fin_year = str(request.GET.get('fin_year', 2015))

        result = {
            'cluster_id': project['cluster_id'],
            'cluster': project['cluster'],
            'name': project['name'],
            'entered_budget': project['total_anticipated_cost'],
            'calculated_budget': project['calculated']['financial_years'][fin_year]['expenditure']['planned_to_date'],
            'entered_expenditure': project['expenditure_to_date'],
            'calculated_expenditure': project['calculated']['financial_years'][fin_year]['expenditure']['actual_to_date'],
            'edit_url': '/entry/%s/edit' % project['project_id'],
            'url' : project['url'],

            'DT_RowId': project['project_id']
        }

        if result['entered_budget'] == 0 or result['entered_expenditure'] == 0:
            result['score'] = '&infin;'
        elif result['entered_budget'] is None or result['entered_expenditure'] is None:
            result['score'] = ''
        else:
            result['score'] = int((result['calculated_budget'] / result['entered_budget'] + result['calculated_expenditure'] / result['entered_expenditure']) * 50)

        return result
    return _map

def map_projects(request, projects, total):
    result = {
        'draw': request.GET.get('draw'),
        'recordsTotal': total,
        'recordsFiltered': projects.hits.total,
        'data': map(create_map(request), projects.hits),
    }
    return result

def diagnose(request):
    fin_year = str(request.GET.get('fin_year', 2015))

    (projects, total) = projects_by_fin_year(request)

    if request.is_ajax():
        response = map_projects(request, projects, total)
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        form = NewIndexForm(request.GET)
        return TemplateResponse(request, 'entry/diagnose.html', {'fin_year': fin_year, 'projects': projects, 'form': form})

def projects(request):
    clusters = {}
    objects = Cluster.objects.all()
    for cluster in objects:
        clusters[cluster.name] = unicode(cluster)

    source = filter_projects(request)

    projects = []
    for p in source:
        if p._uuid:
            if p.cluster:
                if p.cluster in clusters:
                    cluster = clusters[p.cluster]
                else:
                    cluster = p.cluster
            else:
                cluster = None

            project = {
                'uuid': p._uuid,
                'name': p.name,
                'description': p.description,
                'cluster': cluster,
                'programme': p.programme,
                'contract': p.contract,
                'expenditure_to_date': _safe_int(p.expenditure_to_date),
                'total_anticipated_cost': _safe_int(p.total_anticipated_cost),
                'valid_status': p.valid_status
            }

            projects.append(project)

    form = IndexForm(request.GET)

    return TemplateResponse(request, 'entry/list.html', {'projects': projects, 'form': form})

def generate_year(year):
    return [
        { 'expenditure': None, 'progress': None, 'date': '%04d-04-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-05-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-06-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-07-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-08-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-09-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-10-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-11-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-12-01T00:00:00' % (year) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-01-01T00:00:00' % (year+1) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-02-01T00:00:00' % (year+1) },
        { 'expenditure': None, 'progress': None, 'date': '%04d-03-01T00:00:00' % (year+1) },
    ]
    
def new(request):
    year = datetime.today().year
    month = datetime.today().month
    if month < 3:
        year -= 1

    details = {
        'planning': generate_year(year),
        'actual': generate_year(year),
    }

    project = Project(details)

    cluster_id = request.GET.get('cluster')
    if cluster_id and cluster_id != 'None':
        cluster = Cluster.objects.get(id=cluster_id)
        project._details['cluster'] = cluster.name

    project.edit = True
    project.save()

    return redirect('entry:edit', project_id=project._uuid)

def _find_or_add_month(data, year, month):
    for entry in data:
        try:
            d = iso8601.parse_date(entry['date'])
        except:
            pass
        else:
            if d.year == year and d.month == month:
                return
    data.append({
        'expenditure': None,
        'progress': None,
        'date': '%04d-%02d-01T00:00:00' % (year, month)
    })
        

def edit(request, project_id):
    project = Project.edit(project_id)
    # Check actual and planned monthly entries. Add any required to
    # get to this financial year.
    for year_diffs in xrange(2, 0, -1):
        current = datetime.today() - timedelta(weeks=year_diffs * 52)

        for m in range(3, 15):
            year = current.year
            if current.month < 3:
                year -= 1
            if project.actual == '':
                project._details['actual'] = generate_year(year)
            if project.planning == '':
                project._details['planning'] = generate_year(year)

            year += m / 12
            month = m % 12 + 1

            _find_or_add_month(project.actual, year, month)
            _find_or_add_month(project.planning, year, month)

    project._details['actual'] = sorted(project._details['actual'], key=lambda p: p['date'])
    project._details['planning'] = sorted(project._details['planning'], key=lambda p: p['date'])
        
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key == '__reset':
                project.clear()
                project = Project.edit(project_id)
            elif key == '__save':
                project.edit = False
            elif key == 'csrfmiddlewaretoken':
                pass
            else:
                keys = key.split('.')
                if len(keys) == 1:
                    project._details[keys[0]] = value
                else:
                    keys.reverse()
                    d = project._details
                    while len(keys) > 1:
                        k = keys.pop()
                        if type(d) == type({}):
                            d = d.get(k)
                        elif type(d) == type([]):
                            d = d[int(k)]
                        else:
                            pass
                    d[keys[0]] = value
        project._details['last_modified_user'] = request.user.username if request.user.is_authenticated() else ''
        project._details['last_modified_time'] = datetime.now().isoformat()
        project.save()
        return HttpResponse(json.dumps(project._details), mimetype='application/json')

    cluster = Cluster.objects.get(name=project.cluster)
    project._details['__project_url'] = reverse('reports:project', kwargs={ 'project_id': project._uuid })

    context = {
        'cluster': cluster,
        'data': json.dumps(project._details),
        'clusters': Cluster.objects.all(),
        'implementing_agents': ImplementingAgent.objects.all(),
        'municipalities': list(Municipality.objects.all().values_list('name', flat=True))
    }
    return TemplateResponse(request, 'entry/project.html', context)

@csrf_exempt
def contractor(request):
    query = request.POST.get('query')
    if not query:
        return HttpResponse(json.dumps([]), mimetype='application/json')
    project_list = (Project.get(uuid) for uuid in Project.list())
    result = [ p.contractor for p in project_list if re.search(query, p.contractor, re.IGNORECASE) ]
    return HttpResponse(json.dumps(result), mimetype='application/json')
        
@csrf_exempt
def coordinator(request):
    query = request.POST.get('query')
    if not query:
        return HttpResponse(json.dumps([]), mimetype='application/json')
    project_list = (Project.get(uuid) for uuid in Project.list())
    result = [ p.manager for p in project_list if re.search(query, p.manager, re.IGNORECASE) ]
    return HttpResponse(json.dumps(result), mimetype='application/json')

@csrf_exempt
def programme(request):
    cluster = request.GET.get('cluster')
    if not cluster:
        return HttpResponse(json.dumps([]), mimetype='application/json')
    programmes = list(Programme.objects.filter(cluster__name=cluster).values_list('name', flat=True))
    return HttpResponse(json.dumps(programmes), mimetype='application/json')

@csrf_exempt
def cluster(request):
    clusters = list(Cluster.objects.all().values('name'))
    return HttpResponse(json.dumps(clusters), mimetype='application/json')

@csrf_exempt
def municipality(request):
    municipalities = list(Municipality.objects.all().values_list('name', flat=True))
    return HttpResponse(json.dumps(municipalities), mimetype='application/json')

@csrf_exempt
def projects_json(request):
    project_list = (Project.get(uuid) for uuid in Project.list())
    projects = [{
        'uuid': p._uuid,
        'name': p.name,
        'description': p.description,
        'contract': p.contract,
        'cluster': p.cluster,
        'municipality': p.municipality,
        'programme': p.programme,
        'phase': (p.phase or '').title(),
        'year': p.fyear
    } for p in project_list]
    years = set((i['year'] for i in projects))
    result = [{
        'year': year,
        'projects': [p for p in projects if p['year'] == year]
    } for year in years]
    return HttpResponse(json.dumps(projects), mimetype='application/json')
