import re
import json as json
import iso8601
import string
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from libs.database.database import Project

from forms import IndexForm
from models import Cluster, Programme, ImplementingAgent

def _safe_int(val, add=0):
    try:
        return int(filter(lambda x: x.isdigit() or x == '.', str(val))) + add
    except (TypeError, ValueError):
        return None

def projects(request):
    cluster_id = request.GET.get('cluster')
    query = request.GET.get('query')

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

    source = filter(
        _filter,
        [Project.get(p) for p in Project.list() if p]
    )

    projects = []
    for p in source:
        if p._uuid:
            if p.cluster:
                cluster = Cluster.objects.get(name=p.cluster)
            else:
                cluster = None

            project = {
                'uuid': p._uuid,
                'name': p.name,
                'description': p.description,
                'cluster': None,
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
        'implementing_agents': ImplementingAgent.objects.all()
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
