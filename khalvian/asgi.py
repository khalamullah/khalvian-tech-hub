import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.devices.routing
import apps.notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khalvian.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            apps.devices.routing.websocket_urlpatterns +
            apps.notifications.routing.websocket_urlpatterns
        )
    ),
})