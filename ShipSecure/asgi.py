"""
ASGI config for ShipSecure project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.urls import path
from django.core.asgi import get_asgi_application
from shipment.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShipSecure.settings')


application = get_asgi_application()

websocket_urlpatterns = [
    path('ws/Shipment/<str:room_id>/', MyConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns)
})
