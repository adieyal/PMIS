#!/bin/bash

source /etc/bash_completion.d/virtualenvwrapper
workon pmis

cd /home/pmis/deploy

# XXX: Test settings are the only ones I can get to work
python manage.py collectstatic --settings=project.settings.test
