from channels.routing import route
from . import consumers

channel_routing = [
    route('websocket.receive', consumers.ws_message)
]
