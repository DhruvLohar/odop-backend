from .models import Forum

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

class ForumConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.slug = self.scope['url_route']['kwargs']['slug']
        
        if not hasattr(self, 'forum_instance'):
            self.forum_instance = await database_sync_to_async(Forum.objects.get)(slug=self.slug)


        await self.channel_layer.group_add(
            self.slug,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.slug,
            self.channel_name
        )

    @database_sync_to_async
    def save_messages(self, payload):
        try:
            self.forum_instance.addMessage(
                sender=payload.get('uid'), 
                type=payload.get('msg_type'),
                message=payload.get('message'),
                object_id=payload.get('object_id')
            )
        except Exception as err:
            pass

    async def receive_json(self, content, **kwargs):
        uid = content.get("uid")
        message = content.get("message")
        msg_type = content.get("msg_type")
        object_id = content.get("object_id")

        await self.save_messages(content)

        await self.channel_layer.group_send(
            self.slug,
            {
                'type': 'boardcast_in_session',
                'channelID': self.channel_name,
                
                'msg_type': msg_type,
                'uid': uid,
                'object_id': object_id,
                'message': message
            }
        )
        
    async def boardcast_in_session(self, event):
        uid = event['uid']
        message = event['message']
        msg_type = event["msg_type"]
        object_id = event.get("object_id")

        is_same_user = self.channel_name == event['channelID']

        if not is_same_user:
            await self.send_json({
                'uid': uid,
                'message': message,
                'msg_type': msg_type,
                'object_id': object_id,
            })