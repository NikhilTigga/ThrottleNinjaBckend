import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from myapp.models import ChatRoom, ChatMessage
from myapp.models import UserRegisterdb


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        sender_id = data.get("sender_id")
        message = data.get("message")

        chat_message = await self.save_message(
            sender_id,
            message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": chat_message.message,
                "sender_id": sender_id,
                "message_id": chat_message.id,
                "created_at": str(chat_message.created_at)
            }
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "message_id": event["message_id"],
                "sender_id": event["sender_id"],
                "message": event["message"],
                "created_at": event["created_at"]
            })
        )

    @database_sync_to_async
    def save_message(self, sender_id, message):

        room = ChatRoom.objects.get(
            id=self.room_id
        )

        sender = UserRegisterdb.objects.get(
            id=sender_id
        )

        return ChatMessage.objects.create(
            room=room,
            sender=sender,
            message=message
        )