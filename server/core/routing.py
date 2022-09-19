# Router for channels

# Middleware for authenticating users
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing


# To use Django Authentication we wrap websocket with AuthMiddlewareStack
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
      URLRouter(
        routing.websocket_urlpatterns
      )
    )
})