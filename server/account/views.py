
import json as json
from django.http import HttpResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@csrf_exempt
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    
    if not username:
        result = { 
            'success': False,
            'errors': [{
                'field': 'username',
                'error': 'required',
                'description': 'Please enter a username.'
            }]
        }  
        return HttpResponse(json.dumps(result), mimetype='application/json')

    if not password:
        result = { 
            'success': False,
            'errors': [{
                'field': 'password',
                'error': 'required',
                'description': 'Please enter a password.'
            }]
        }  
        return HttpResponse(json.dumps(result), mimetype='application/json')

    
    user = auth.authenticate(username=username, password=password)
    if not user:
        result = { 
            'success': False,
            'errors': [
                {
                    'field': 'username',
                    'error': 'failed',
                    'description': 'The username and password did not match.'
                },
                {
                    'field': 'password',
                    'error': 'failed',
                    'description': 'The username and password did not match.'
                }
            ]
        }  
        return HttpResponse(json.dumps(result), mimetype='application/json')

    auth.login(request, user)
    result = { 
        'success': True
    }  
    return HttpResponse(json.dumps(result), mimetype='application/json')

@csrf_exempt
@login_required
def logout(request):
    auth.logout(request)
    result = { 
        'success': True
    }  
    return HttpResponse(json.dumps(result), mimetype='application/json')

@csrf_exempt
def session(request):
    if request.user.is_authenticated():
        result = { 
            'authenticated': True,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }  
        return HttpResponse(json.dumps(result), mimetype='application/json')
    else:
        result = { 
            'authenticated': False
        }  
        return HttpResponse(json.dumps(result), mimetype='application/json')
        
    
