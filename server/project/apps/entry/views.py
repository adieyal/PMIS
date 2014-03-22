import json
from django.http import HttpResponse
from django.template.response import TemplateResponse
from project.libs.database.database import Project


def list(request):
    project_list = (Project.get(uuid) for uuid in Project.list())
    context = {
        'projects': [{
            'uuid': p._uuid,
            'name': p.name,
            'description': p.description,
            'contract': p.contract
        } for p in project_list]
    }
    return TemplateResponse(request, 'entry/list.html', context)

def project(request, project_id):
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
    context = {
        'data': json.dumps(project._details)
    }
    return TemplateResponse(request, 'entry/project.html', context)
