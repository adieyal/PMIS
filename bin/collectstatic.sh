#!/bin/bash

source /etc/bash_completion.d/virtualenvwrapper
workon pmis

cd /home/pmis/deploy
mkdir -p assets

# XXX: Test settings are the only ones I can get to work
/home/pmis/.virtualenvs/pmis/bin/python manage.py collectstatic --settings=project.settings.test --noinput --clear
