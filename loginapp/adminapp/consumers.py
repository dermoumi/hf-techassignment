import json
from channels import Channel, Group
from channels.sessions import channel_session

@channel_session
def ws_connect_mailjobs(message):
    message.reply_channel.send({
        'accept': True,
        'text': json.dumps({
            'action': 'reply_channel',
            'reply_channel': message.reply_channel.name,
        })
    })

    Group('mailjobs').add(message.reply_channel)

@channel_session
def ws_receive_mailjobs(message):
    data = json.loads(message.content.get('text'))

    if data.get('action') == 'revoke_task':
        from mainapp.models import EmailJob
        from celery.task.control import revoke
        from django.core import serializers

        mail_job = EmailJob.objects.get(pk=data.get('job_pk'))
        revoke(mail_job.celery_id, terminate=True)

        mail_job.status = 'revoked'
        mail_job.save()

        # Notify task changed state (revoked)
        Group('mailjobs').send({
            'text': '{"action": "changed_status", "jobs": %s}' % serializers.serialize('json', [mail_job])
        })

