from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/forum/(?P<slug>[0-9a-f-]+)/$", consumers.ForumConsumer.as_asgi()),
]