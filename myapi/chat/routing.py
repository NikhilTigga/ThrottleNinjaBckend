from django.urls import re_path
from .consumers import ChatConsumer
from .clubconsumer import ClubConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<room_id>\w+)/$",
        ChatConsumer.as_asgi()
    ),
    
    
    re_path(
        r"ws/club/(?P<club_id>\d+)/$",
        ClubConsumer.as_asgi()
    ),
]