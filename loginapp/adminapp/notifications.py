from . import models
from django.utils.translation import ugettext as _
from channels import Group
from django.core import serializers
from mainapp.models import User
from django.core.urlresolvers import reverse

def notify_admins(kind, link, content, admins = None):
    notification = models.Notification(kind=kind, link=link, content=content)
    notification.save()

    if admins is None:
        admins = User.objects.filter(is_admin=True)

    models.UserNotification.objects.bulk_create(
        [models.UserNotification(notification_id=notification.pk, user_id=admin.pk) for admin in admins]
    )
 
    # Notify admins
    Group('admin').send({
        'text': '{"action": "notification", "notifications": %s}' % serializers.serialize('json', [notification])
    })

def mail_job_created(mail_job):
    Group('mailjobs').send({
        'text': '{"action": "created", "jobs": %s}' % serializers.serialize('json', [mail_job])
    })

    notify_admins(kind='mail_job_created', link=reverse('adminapp:mailjobs_all'),
        content=_('A new mail job to «%s» was created') % mail_job.destination)

def mail_job_changed_status(mail_job):
    Group('mailjobs').send({
        'text': '{"action": "changed_status", "jobs": %s}' % serializers.serialize('json', [mail_job])
    })

    # Probably don't need to notify status changes? or probably just some of them?
    # notify_admins(kind='mail_job_changed_status', link=reverse('adminapp:mailjobs_all'),
    #     content=_('Mail job to «%s» changed status to «%s»') % (mail_job.destination, mail_job.status))
