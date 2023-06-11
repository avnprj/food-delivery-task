import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import food_delivery.routing  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            food_delivery.routing.websocket_urlpatterns
        )
    ),
})
