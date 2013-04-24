#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from provy.core import Role, AskFor
from provy.more.debian import UserRole, NginxRole
from provy.more.debian import GitRole, MySQLRole
from provy.more.debian import SupervisorRole

from roles.django import UpdatedDjangoRole

USER = "pmis"
USER_HOME = "/home/pmis"
LOG_DIR = os.path.join(USER_HOME, "logs")
STATIC_DIR = os.path.join(USER_HOME, "site-media", "static")
PROJECT_HOME = os.path.join(USER_HOME, "django-tutorial", "mysite")


class DjangoWebSite(Role):
    def symlink_folder(self, from_dir, to_dir, sudo=True):
        """
        Similar to remote_symlink except that method does not allow for directory symlinks
        """
        if not self.remote_exists_dir(from_dir):
            raise RuntimeError("The dir to create a symlink from (%s) was not found!" % from_dir)

        command = 'ln -sf %s %s' % (from_dir, to_dir)
        if self.remote_exists_dir(to_dir):
            result = self.execute('ls -la %s' % to_dir, stdout=False, sudo=sudo)
            if '->' in result:
                path = result.split('->')[-1].strip()
                if path != from_dir:
                    self.log('Symlink has different path(%s). Syncing...' % path)
                    self.execute(command, stdout=False, sudo=sudo)
        else:
            self.log('Symlink not found at %s! Creating...' % from_dir)
            self.execute(command, stdout=False, sudo=sudo)

    def provision(self):


        with self.using(UserRole) as role:
            role.ensure_user(USER, identified_by="pass", is_admin=True)

        with self.using(GitRole) as role:
            role.ensure_repository(
                repo="git://github.com/heynemann/django-tutorial.git",
                path="/home/pmis/django-tutorial",
                branch="master",
                owner=USER
            )

        self.ensure_dir(LOG_DIR, sudo=True, owner=USER)
        self.ensure_dir(STATIC_DIR, sudo=True, owner=USER)

        with self.using(MySQLRole) as role:
            role.ensure_user(
                username=self.context["mysql_user"],
                login_from="%",
                identified_by=self.context["mysql_password"]
            )

            role.ensure_database(self.context["mysql_database"])
            role.ensure_grant(
                "ALL PRIVILEGES", 
                on=self.context["mysql_database"],
                username=self.context["mysql_user"],
                login_from="%"
            )

            role.ensure_user(
                username=self.context["mysql_user"],
                login_from="localhost",
                identified_by=self.context["mysql_password"]
            )

            role.ensure_grant(
                "ALL PRIVILEGES", 
                on=self.context["mysql_database"],
                username=self.context["mysql_user"],
                login_from="localhost"
            )

        with self.using(SupervisorRole) as role:
            role.config(
                config_file_directory=USER_HOME,
                log_folder=LOG_DIR,
                user=USER
            )

            with self.using(UpdatedDjangoRole) as role:
                role.restart_supervisor_on_changes = True
                with role.create_site("website") as site:
                    site.use_supervisor = True
                    site.settings_path = os.path.join(PROJECT_HOME, "settings.py")
                    #site.environment = "DJANGO_SETTINGS_MODULE=local_settings.py"
                    site.threads = 2
                    site.processes = 4
                    site.user = "pmis"
                    site.pid_file_path = USER_HOME
                    site.log_file_path = LOG_DIR
                    site.settings_module = "local_settings"
                    site.settings = {
                        'DATABASES["default"]["NAME"]' : self.context["mysql_database"],
                        'DATABASES["default"]["USER"]' : self.context["mysql_user"],
                        'DATABASES["default"]["PASSWORD"]' : self.context["mysql_password"],
                        'STATIC_ROOT' : STATIC_DIR
                    }

        with self.using(NginxRole) as role:
            role.ensure_conf(conf_template="nginx.conf")
            role.ensure_site_disabled("default")
            role.create_site(site="pmis", template="pmis")
            role.ensure_site_enabled("pmis")


        # Symlink the admin app assets into static/admin
        self.symlink_folder(
            "/usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin/", 
            os.path.join(STATIC_DIR, "admin")
        )


servers = {
    "local" : {
        "web" : {
            "address" : "33.33.33.33",
            "user" : "vagrant",
            "roles" : [
                DjangoWebSite,
            ],
            "options" : {
                "mysql_root_pass" : "pass",
                "mysql_user" : "pmis",
                "mysql_password" : AskFor("mysql_password", "Please enter the password for the mysql user"),
                "mysql_database" : "pmis"
            }
        },
    }
}
