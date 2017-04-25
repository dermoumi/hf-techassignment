import time, json, logging
from channels import Channel
from loginapp.celery import app
from . import models

log = logging.getLogger(__name__)

@app.task
def sec3(job_id, reply_channel):
    # time sleep represent some long running process
    time.sleep(3)

    # Change task status to completed
    job = models.Job.objects.get(pk=job_id)
    log.debug('Running job_name = %s', job.name)

    job.status = 'completed'
    job.save()

    # Send status update back to browser client
    if reply_channel is not None:
        Channel(reply_channel).send({
            'text': json.dumps({
                'action': 'completed',
                'job_id': job.id,
                'job_name': job.name,
                'job_status': job.status
            })
        })
