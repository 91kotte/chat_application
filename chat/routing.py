# chat/routing.py -> defines the URL routing for WebSocket connections in a Django Channels application.
from django.urls import re_path  #This is a Django function used for URL routing. It allows you to specify regular expressions (regex) to match specific URL patterns.
from . import consumers

# To route WebSocket connections to the appropriate consumer
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
