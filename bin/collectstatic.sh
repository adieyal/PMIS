#!/bin/bash
source /etc/bash_completion.d/virtualenvwrapper

workon pmis
cd /home/pmis/deploy
python manage.py collectstatic
