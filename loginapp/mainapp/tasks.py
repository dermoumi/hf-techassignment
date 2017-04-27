import time, json, logging
from channels import Channel
from celery import shared_task, Task
from django.utils import timezone
from django.core.mail import send_mail
from smtplib import SMTPException
from celery.exceptions import MaxRetriesExceededError
from . import models
from adminapp import notifications

log = logging.getLogger(__name__)

class NotifyErrorSharedTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Failed to send (max retries exceeded)
        log.error('Email task failed: %s', exc)
        mail_job = models.EmailJob.objects.get(celery_id=task_id)
        mail_job.status = 'failed'
        mail_job.save()

        notifications.mail_job_changed_status(mail_job)

        super(NotifyErrorSharedTask, self).on_failure(exc, task_id, args, kwargs, einfo)

def send_email(destination):
    log.debug('Mail job to %s', destination)

    mail_job = models.EmailJob(destination=destination)
    mail_job.save()

    notifications.mail_job_created(mail_job)

    # Start task
    task = send_email_task.delay(mail_job.id)
    
    mail_job.celery_id = task.id
    mail_job.save()

@shared_task(bind=True, base=NotifyErrorSharedTask)
def send_email_task(self, job_id):
    # Wait a little before starting
    time.sleep(1)

    mail_job = models.EmailJob.objects.get(pk=job_id)
    log.debug('Running mail job to %s', mail_job.destination)
    mail_job.status = 'started'
    mail_job.save()

    notifications.mail_job_changed_status(mail_job)

    try:
        # Attempt to send email
        send_mail(
            'Confirmation email',
            'You have successfully signed up',
            'test@gmail.com',
            [mail_job.destination],
            fail_silently=False
        )

        time.sleep(1) # TODO: Remove this

    except Exception as message:
        # On error, log and retry
        log.error('Error sending mail: %s', message)
        mail_job.status = 'retrying'
        if self.max_retries is None or mail_job.retry_count < self.max_retries:
            mail_job.retry_count += 1
        mail_job.last_retry_at = timezone.now()
        mail_job.save()

        notifications.mail_job_changed_status(mail_job)

        self.retry(countdown=1) # TODO: Restore countdown to 60 * 5

    else:
        # Everything went fine
        mail_job.status = 'success'
        mail_job.save()

        notifications.mail_job_changed_status(mail_job)
