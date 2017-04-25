from channels.routing import route

channel_routing = [
    route('http.request', 'mainapp.consumers.http_consumer')
]
