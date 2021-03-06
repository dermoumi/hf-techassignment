#!/bin/sh

# wait for other servers to start
sleep 10

# Run celery worker with log level set to DEBUG
su -m myuser -c "celery --app=loginapp.celery:app worker --loglevel=DEBUG"