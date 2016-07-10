#!/bin/bash
UNI=/Users/windson/uni/srv/unicooo/www
cd $UNI
python3 manage.py runserver --settings=unicooo.settings.local
