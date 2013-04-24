from provy.more.debian import django
from os.path import dirname

SITES_KEY = 'django-sites'

class UpdatedDjangoRole(django.DjangoRole):

    def provision(self):
        self.register_template_loader('roles')
        super(UpdatedDjangoRole, self).provision()

    def cleanup(self):
        super(UpdatedDjangoRole, self).cleanup()

        if SITES_KEY in self.context:
            for website in self.context[SITES_KEY]:
                updated = self.__update_init_script(website)


    def __update_init_script(self, website):
        at_least_one_updated = False
        for process_number in range(website.processes):
            port = website.starting_port + process_number
            options = {
                'name': website.name,
                'pid_file_path': website.pid_file_path.rstrip('/'),
                'user': website.user,
                'host': website.host,
                'port': port,
                'threads': website.threads,
                'daemon': website.daemon,
                'user': website.user,
                'settings_directory': dirname(website.settings_path),
                'settings_module': website.settings_module,
            }
            script_name = '%s-%d' % (website.name, port)
            result = self.update_file('website.init.template', '/etc/init.d/%s' % script_name, owner=website.user, options=options, sudo=True)

            if result:
                at_least_one_updated = True
                self.execute('chmod +x /etc/init.d/%s' % script_name, stdout=False, sudo=True)
                if website.auto_start:
                    self.execute('update-rc.d %s defaults' % script_name, stdout=False, sudo=True)

        return at_least_one_updated
    
