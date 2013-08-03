from fabric.api import run, local, settings, cd, env, sudo
from fabric.contrib.console import confirm

env.hosts = ["adi@pmis.burgercom.co.za:2224"]
def host_type():
    run('uname -s')

def commit():
    with settings(warn_only=True):
        result = local("git add -p && git commit", capture=True)
    if result.failed and not confirm("Error with commit. Continue anyway?"):
        abort("Aborting at user request.")

def test():
    local("server/manage.py test api projects")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = "/var/www/pmis.burgercom.co.za"
    with cd(code_dir):
        run("git pull origin master")
    with cd(code_dir + "/server"):
        run("/home/adi/.virtualenvs/pmis/bin/pip install -r requirements/test.txt")
        sudo("supervisorctl restart pmis")
