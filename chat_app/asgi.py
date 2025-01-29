"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# configures ASGI (Asynchronous Server Gateway Interface) for a Django application using Django Channels to handle both HTTP and WebSocket protocols
import os
from django.core.asgi import get_asgi_application # default ASGI application for handling HTTP requests.
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack #middleware stack that adds authentication support for WebSocket connections
from chat import routing  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')


# Initialize the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
