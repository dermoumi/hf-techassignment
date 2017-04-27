from channels import Channel, Group
from channels.sessions import channel_session
import json

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