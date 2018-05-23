#!/bin/bash

workon mxonline
cd ~/projects/GMOOC/gmooc
git pull
python manage.py migrate
pkill uwsgi
