# Don't forget to set DJANGO_SETTINGS_MODULE as needed
# e.g. export DJANGO_SETTINGS_MODULE=project.settings.local
createdatabase:
	rm -f project/default.db
	python manage.py syncdb --noinput
	python manage.py migrate
	python manage.py loaddata production
	python manage.py createsuperuser

loaddata:
	python scripts/process_idp.py "/home/adi/Dropbox/IDIP Reports/2013/DoE/June.xls" 2013 6 > /tmp/projects.json
	python manage load_projects /tmp/projects.json

