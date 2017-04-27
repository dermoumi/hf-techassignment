from channels.routing import route
from adminapp.consumers import ws_connect_mailjobs, ws_receive_mailjobs

channel_routing = [
    route('websocket.connect', ws_connect_mailjobs, path=r'^/mailjobs/$'),
    route('websocket.receive', ws_receive_mailjobs, path=r'^/mailjobs/$'),
]
