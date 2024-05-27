#!/bin/sh
cd server
celery -A server beat -l info