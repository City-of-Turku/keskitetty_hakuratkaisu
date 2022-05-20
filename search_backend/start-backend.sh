#!/usr/bin/env bash

python ./src/setup.py $elastic_admin_username $elastic_admin_password
service nginx start
cd src
uwsgi --ini ../uwsgi.ini --file ./server.py
