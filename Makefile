createdatabase:
	python manage.py syncdb --noinput
	python manage.py migrate
	python manage.py createsuperuser
