from fabric.api import *
from fabric.contrib import *

venv = '/home/marlinf/.virtualenvs/pmis/bin/activate'

env.use_ssh_config = True
env.hosts = ['pmis']

env.instances = {
        'demo': {
            'BASE_URL': 'http://pmis-demo.burgercom.co.za',
            'SECRET_KEY': '34234v*eh#_gq618si+0gucd!fpkr2n07gxuy4m$mg_ss&_0h-ktm1fgdf',
        },
        'production': {
            'BASE_URL': 'http://pmis.burgercom.co.za',
            'SECRET_KEY': '34234v*eh#_gq618si+0gucd!fpkr2n07gxuy4m$mg_ss&_0h-ktm1fgdf',
        }
}

def deploy():
    for instance, instance_env in env.instances.iteritems():
        with cd('/var/www/%s' % instance):
            run('git pull --ff-only')

            with shell_env(**instance_env), cd('server'), prefix('source ' + venv):
                run('python manage.py syncdb')
                run('python manage.py migrate')
                run('python manage.py collectstatic --noinput')

        sudo('supervisorctl restart %s' % instance)
