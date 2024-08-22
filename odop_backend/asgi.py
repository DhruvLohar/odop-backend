"""
ASGI config for Piikeup project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os, django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odop_backend.settings')
django.setup()

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from forum.routing import websocket_urlpatterns as forumRoutes
# from messenger.routing import websocket_urlpatterns as messengerWebsocketUrls
# from rider.routing import websocket_urlpatterns as riderWebsokcetUrls

websockets_urls = forumRoutes

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websockets_urls))
        ),
    }
)