from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user1>\w+)/(?P<user2>\w+)/$', consumers.ChatConsumer),
]