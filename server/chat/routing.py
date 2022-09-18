from django.urls import re_path
from chat import consumer

websocket_urlpatterns = [
  re_path(r'ws/chat/(?P<room>\w+)/$', consumer.ChatRoomConsumer)
]