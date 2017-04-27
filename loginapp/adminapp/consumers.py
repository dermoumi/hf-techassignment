import json
from channels import Channel, Group
from channels.auth import channel_session_user_from_http, channel_session_user
from . import models

@channel_session_user_from_http
def ws_connect_mailjobs(message):
    if not message.user.is_authenticated() or not message.user.is_staff:
        return

    message.reply_channel.send({
        'accept': True,
        'text': json.dumps({
            'action': 'reply_channel',
            'reply_channel': message.reply_channel.name,
        })
    })

    Group('mailjobs').add(message.reply_channel)

@channel_session_user
def ws_receive_mailjobs(message):
    if not message.user.is_authenticated() or not message.user.is_staff:
        return
    
    data = json.loads(message.content.get('text'))

    if data.get('action') == 'revoke_task':
        from mainapp.models import EmailJob
        from celery.task.control import revoke
        from django.core import serializers

        mail_job = EmailJob.objects.get(pk=data.get('job_pk'))
        revoke(mail_job.celery_id, terminate=True)

        mail_job.status = 'revoked'
        mail_job.save()

        from . import notifications
        notifications.mail_job_changed_status(mail_job)

@channel_session_user_from_http
def ws_connect_admin(message):
    if not message.user.is_authenticated() or not message.user.is_staff:
        return

    # Send out the number of unread notifications while at it
    unread_notifications = models.UserNotification.objects.filter(user_id=message.user.pk, unread=True)

    message.reply_channel.send({
        'accept': True,
        'text': json.dumps({
            'action': 'reply_channel',
            'reply_channel': message.reply_channel.name,
            'unread_notification_count': unread_notifications.count()
        })
    })

    Group('admin').add(message.reply_channel)
    Group('admin-%s' % message.user.pk).add(message.reply_channel)

@channel_session_user
def ws_receive_admin(message):
    if not message.user.is_authenticated() or not message.user.is_staff:
        return
    
    data = json.loads(message.content.get('text'))
    print('DATA =', data)

    if data.get('action') == 'notification_read':
        # Mark notification as count
        user_id = message.user.pk
        notification_id = data.get('notification_id')
        user_notification = models.UserNotification.objects.get(user_id=user_id, notification_id=notification_id)
        user_notification.unread = False
        user_notification.save()

        Group('admin-%s' % user_id).send({
            'text': '{"action": "notification_read", "notification_id": %s}' % notification_id
        })

    elif data.get('action') == 'notification_all_read':
        # Mark all notifications as read
        user_id = message.user.pk
        user_notifications = models.UserNotification.objects.filter(user_id=user_id, unread=True).update(unread=False)

        Group('admin-%s' % user_id).send({
            'text': '{"action": "notification_all_read"}'
        })
