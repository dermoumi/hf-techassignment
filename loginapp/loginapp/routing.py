from channels.routing import route
from adminapp import consumers as admin_consumers

channel_routing = [
    route('websocket.connect', admin_consumers.ws_connect_mailjobs, path=r'^/mailjobs/$'),
    route('websocket.receive', admin_consumers.ws_receive_mailjobs, path=r'^/mailjobs/$'),
    route('websocket.connect', admin_consumers.ws_connect_admin, path=r'^/admin/$'),
    route('websocket.receive', admin_consumers.ws_receive_admin, path=r'^/admin/$'),
]
