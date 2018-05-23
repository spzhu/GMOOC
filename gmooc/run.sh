#!/bin/bash

workon mxonline
cd ~/projects/GMOOC/gmooc
git fetch --all
git reset --hard origin/master
git pull
python manage.py migrate
pkill uwsgi

exit 0
