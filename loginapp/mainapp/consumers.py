from django.http import HttpResponse
from channels.sessions import channel_session
from channels import Group
from .tasks import sec3
from . import models
import json, logging

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    message.reply_channel.send({
        'text': json.dumps({
            'action': 'reply_channel',
            'reply_channel': message.reply_channel.name
        })
    })

@channel_session
def ws_receive(message):
    try:
        data = json.loads(message.get('text'))
    except ValueError:
        log.debug('ws message is not json text = %s', message.get('text'))
        return

    if data:
        reply_channel = message.reply_channel.name

        if data.get('action') == 'start_sec3':
            start_sec3(data, reply_channel)

def start_sec3(data, reply_channel):
    log.debug('Job name = %s', data.get('job_name'))

    # Save model to our database
    job = models.Job(name=data.get('job_name'), status='started')
    job.save()

    # Start long running task here (using Celery)
    sec3_task = sec3.delay(job.id, reply_channel)

    # Store the celery task id into the database if we wanted to do things
    # like cancelling it in the future
    job.celery_id = sec3_task.id
    job.save()

    # Tell the client that the task has been started
    Channel(reply_channel).send({
        'text': json.dumps({
            'action': 'started',
            'job_id': job.id,
            'job_name': job.name,
            'job_status': job.status,
        })
    })
