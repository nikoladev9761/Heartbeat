import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import heartbeat_app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "heartbeat.settings")

application = ProtocolTypeRouter({  
  "http": get_asgi_application(),  
  "websocket": AuthMiddlewareStack(     
        URLRouter(  
            heartbeat_app.routing.websocket_urlpatterns
        )
    ),
})