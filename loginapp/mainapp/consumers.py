from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group

def ws_message(message):
    # ASGI webSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    message.reply_channel.send({
        "text": message.content['text']
    })

def ws_connect(mesasge):
    # Accept the incoming connection
    message.reply_channel.send({'accept': True})

    # Add them to the chat group
    Group('chat').add(message.reply_channel)

def ws_disconnect(message):
    Group('chat').discard(message.reply_channel)
