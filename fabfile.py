from fabric.api import *
from fabric.contrib import *

base_dir = '/var/www/PMIS'
django_dir = base_dir + '/server'
venv = '/home/adi/.virtualenvs/pmis/bin/activate'

env.use_ssh_config = True
env.hosts = ['pmis']

def deploy():
    with cd(base_dir):
        run('git pull')
    with cd(django_dir):
        with prefix('source ' + venv):
            run('python manage.py syncdb')
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput')
    with cd(base_dir):
        sudo('supervisorctl restart pmis')
