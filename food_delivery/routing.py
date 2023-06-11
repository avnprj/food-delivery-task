
from django.urls import re_path
from api.consumers import OrderStatusConsumer

websocket_urlpatterns = [
    re_path(r'ws/order/(?P<pk>.*)/$', OrderStatusConsumer.as_asgi()),
]
