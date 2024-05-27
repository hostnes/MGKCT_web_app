#!/bin/sh
cd server
celery -A server worker -l info