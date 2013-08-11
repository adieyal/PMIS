from fabric import api
from fabric.contrib.console import confirm
from fabric import operations
import urllib2

api.env.hosts = ["adi@pmis.burgercom.co.za:2227"]
trigger_url = "http://hudson.burgercom.co.za/job/PMIS/build"
code_dir = "/var/www/PMIS/server"
env_dir = "/home/adi/.virtualenvs/pmis"
python = "%s/bin/python" % env_dir

def host_type():
    api.run('uname -s')

def commit():
    with api.settings(warn_only=True):
        result = api.local("git add -p && git commit", capture=True)
    if result.failed and not confirm("Error with commit. Continue anyway?"):
        abort("Aborting at user request.")

def test():
    api.local("server/manage.py test api projects")

def push():
    api.local("git push")


def migrate():
    with api.cd(code_dir):
        api.run("%s manage.py migrate" % python)

def create_database():
    with api.cd(code_dir):
        api.run("rm -f project/default.db")
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
    with api.cd(code_dir + "/server"):
        api.run("/home/adi/.virtualenvs/pmis/bin/pip install -r requirements/test.txt")
        api.sudo("supervisorctl restart pmis")
    trigger_hudson()

def trigger_hudson():
    urllib2.urlopen(trigger_url)
