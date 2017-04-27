from channels.routing import route
from adminapp.consumers import ws_connect_mailjobs

channel_routing = [
    route('websocket.connect', ws_connect_mailjobs, path=r'^/mailjobs/$'),
]
