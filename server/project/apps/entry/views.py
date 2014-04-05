import re
import json
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from project.libs.database.database import Project

from models import Cluster, Programme, ImplementingAgent


def projects(request):
    project_list = (Project.get(uuid) for uuid in Project.list())
    context = {}
    for p in project_list:
        cluster = p.cluster or 'Unknown'
        if context.get(cluster) == None:
            context[cluster] = []
        context[cluster].append({
            'uuid': p._uuid,
            'name': p.name,
            'description': p.description,
            'contract': p.contract
        })

    return TemplateResponse(request, 'entry/list.html', {'projects': context})
    
def new(request):
    details = {
        'planning': [
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
        ],
        'actual': [
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
            { 'expenditure': None, 'progress': None },
        ]
    }
    project = Project(details)
    project.edit = True
    project.save()
    return redirect('entry:edit', project_id=project._uuid)

def edit(request, project_id):
    project = Project.edit(project_id)
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
    project._details['__project_url'] = reverse('reports:project', kwargs={ 'project_id': project._uuid })
    context = {
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
