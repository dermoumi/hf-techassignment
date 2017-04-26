#!/bin/sh

# wait for other services to start
sleep 3

# Run celery worker with log level set to DEBUG
su -m myuser -c "pytest"