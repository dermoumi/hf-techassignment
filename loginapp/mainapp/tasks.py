import time, json, logging
from channels import Channel
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from smtplib import SMTPException
from . import models

log = logging.getLogger(__name__)

def send_email(destination):
    log.debug('Mail job to %s', destination)

    job = models.EmailJob(destination=destination)
    job.save()

    task = send_email_task.delay(job.id)
    
    job.celery_id = task.id
    job.save()

@shared_task(bind=True)
def send_email_task(self, job_id):
    mail_job = models.EmailJob.objects.get(pk=job_id)
    log.debug('Running mail job to %s', mail_job.destination)

    # TODO: Send notification?
    try:
        # Attempt to send email
        send_mail(
            'Confirmation email',
            'You have successfully signed up',
            'test@gmail.com',
            [mail_job.destination],
            fail_silently=False
        )
    except Exception as message:
        # On error, log and retry
        log.error('Error sending mail: %s', message)
        self.retry(countdown=60 * 5)
        mail_job.retry_count += 1
        mail_job.last_retry_at = timezone.now()
        mail_job.save()
    else:
        # Everything went fine
        mail_job.sent = True
        mail_job.save()
