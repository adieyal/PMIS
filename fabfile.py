from fabric import api
from fabric.contrib.console import confirm
from fabric.context_managers import settings
from fabric import operations
import urllib2

api.env.hosts = ["adi@pmis.burgercom.co.za:2227"]
trigger_url = "http://hudson.burgercom.co.za/job/PMIS/build"
code_dir = "/var/www/PMIS/server"
env_dir = "/home/adi/.virtualenvs/pmis"
python = "%s/bin/python" % env_dir
pip = "%s/bin/pip" % env_dir

def package_installed(pkg_name):
    """ref: http:superuser.com/questions/427318/#comment490784_427339"""
    cmd_f = 'dpkg-query -l "%s" | grep -q "^.i"'
    cmd = cmd_f % (pkg_name)
    with settings(warn_only=True):
        result = api.run(cmd)
    return result.succeeded

def yes_install(pkg_name):
    """ref: http://stackoverflow.com/a/10439058/1093087"""
    api.sudo('apt-get --force-yes --yes install %s' % (pkg_name))

def host_type():
    api.run('uname -s')

def make_sure_memcached_is_installed_and_running():
    if not package_installed('memcached'):
        yes_install('memcached')
    with settings(warn_only=True):
        api.sudo('/etc/init.d/memcached restart', pty=False)

def install_prerequisites():
    make_sure_memcached_is_installed_and_running()

def test():
    api.local("server/manage.py test api projects reports")

def push():
    api.local("git push")

def migrate():
    with api.cd(code_dir):
        api.run("%s manage.py migrate --noinput" % python)

def restart():
    api.sudo("supervisorctl update")
    api.sudo("supervisorctl restart pmis")

def create_database():
    with api.cd(code_dir):
        api.run("rm -f project/default.db --quiet")
        api.run("%s manage.py syncdb --noinput" % python)
        migrate()
        api.run("%s manage.py loaddata production" % python)
        api.run("%s manage.py createsuperuser" % python)
        api.run("%s scripts/process_idp.py ../data/June.xls 2013 6 > /tmp/projects.json" % python)
        api.run("%s manage.py load_projects /tmp/projects.json --traceback" % python)


def deploy():
    """
    Deploy code and run tests in hudson
    """
    with api.cd(code_dir):
        api.run("git pull origin master")
        api.run("%s install -r requirements/test.txt --quiet" % pip)
        migrate()
        api.run("%s manage.py collectstatic --noinput" % python)
        api.run("%s manage.py fixdata" % python)
        restart()
    #trigger_hudson()

def trigger_hudson():
    urllib2.urlopen(trigger_url)
