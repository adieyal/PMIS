# Don't forget to set DJANGO_SETTINGS_MODULE as needed
# e.g. export DJANGO_SETTINGS_MODULE=project.settings.local
createdatabase:
	python manage.py syncdb --noinput
	python manage.py migrate
	python manage.py loaddata production
	python manage.py createsuperuser
