from .models import ChatSession


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

class ForumConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.forum_id = self.scope['url_route']['kwargs']['forum_id']
        
        if not hasattr(self, 'session_instance'):
            self.session_instance = await database_sync_to_async(ChatSession.objects.get)(session_key=self.session_id)


        await self.channel_layer.group_add(
            self.session_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.session_id,
            self.channel_name
        )

    @database_sync_to_async
    def get_connected_users_count(self):
        channel_layer = get_channel_layer()
        group_channels = async_to_sync(channel_layer.group_channels)('online_users')
        return len(group_channels)

    @database_sync_to_async
    def save_messages(self, payload):
        try:
            self.session_instance.addMessage(
                sender=payload.get('uid'), 
                message=payload.get('message')
            )
        except Exception as err:
            pass

    async def receive_json(self, content, **kwargs):
        uid = content.get("uid")
        message = content.get("message")

        await self.save_messages(content)

        await self.channel_layer.group_send(
            self.session_id,
            {
                'type': 'boardcast_in_session',
                'channelID': self.channel_name,
                'uid': uid,
                'message': message
            }
        )
        
    async def boardcast_in_session(self, event):
        uid = event['uid']
        message = event['message']

        is_same_user = self.channel_name == event['channelID']

        if not is_same_user:
            await self.send_json({
                'uid': uid,
                'message': message,
                'users_online': self.channel_layer.receive_count
            })