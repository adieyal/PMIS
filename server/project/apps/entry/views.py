import re
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from project.libs.database.database import Project


def list(request):
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
        project.save()
        return HttpResponse(json.dumps(project._details), mimetype='application/json')
    project._details['__project_url'] = reverse('reports:project', kwargs={ 'project_id': project._uuid })
    context = {
        'data': json.dumps(project._details)
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
