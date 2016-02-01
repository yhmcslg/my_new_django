#!/bin/bash

gunicorn offer.wsgi:application  -D -b 192.168.1.14:9090  -w 8  -k gevent 

