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

        # Send latest 20 messages
        messages = await self.get_last_messages()

        await self.send(
            text_data=json.dumps({
                "type": "chat_history",
                "messages": messages
            })
        )

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        event_type = data.get("type")

        # ==========================
        # SEND MESSAGE
        # ==========================
        if event_type == "message":

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
                    "message_id": chat_message.id,
                    "sender_id": sender_id,
                    "message": chat_message.message,
                    "is_read": False,
                    "created_at": str(chat_message.created_at)
                }
            )

        # ==========================
        # TYPING
        # ==========================
        elif event_type == "typing":

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_event",
                    "sender_id": data.get("sender_id")
                }
            )

        # ==========================
        # STOP TYPING
        # ==========================
        elif event_type == "stop_typing":

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "stop_typing_event",
                    "sender_id": data.get("sender_id")
                }
            )

        # ==========================
        # MESSAGE SEEN
        # ==========================
        elif event_type == "seen":

            message_id = data.get("message_id")

            await self.mark_message_seen(
                message_id
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message_seen",
                    "message_id": message_id
                }
            )

    # =====================================
    # NEW CHAT MESSAGE
    # =====================================
    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "message",
                "message_id": event["message_id"],
                "sender_id": event["sender_id"],
                "message": event["message"],
                "is_read": event["is_read"],
                "created_at": event["created_at"]
            })
        )

    # =====================================
    # TYPING
    # =====================================
    async def typing_event(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "typing",
                "sender_id": event["sender_id"]
            })
        )

    # =====================================
    # STOP TYPING
    # =====================================
    async def stop_typing_event(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "stop_typing",
                "sender_id": event["sender_id"]
            })
        )

    # =====================================
    # MESSAGE SEEN
    # =====================================
    async def message_seen(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "seen",
                "message_id": event["message_id"]
            })
        )

    # =====================================
    # SAVE MESSAGE
    # =====================================
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

    # =====================================
    # MARK SEEN
    # =====================================
    @database_sync_to_async
    def mark_message_seen(self, message_id):

        ChatMessage.objects.filter(
            id=message_id
        ).update(
            is_read=True
        )

    # =====================================
    # LAST 20 MESSAGES
    # =====================================
    @database_sync_to_async
    def get_last_messages(self):

        messages = (
            ChatMessage.objects
            .filter(room_id=self.room_id)
            .select_related("sender")
            .order_by("-created_at")[:20]
        )

        data = []

        for msg in reversed(messages):

            data.append({
                "message_id": msg.id,
                "sender_id": msg.sender.id,
                "sender_name": msg.sender.nick_name,
                "message": msg.message,
                "is_read": msg.is_read,
                "created_at": str(msg.created_at)
            })

        return data


# class ChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):

#         try:

#             self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

#             self.room_group_name = f"chat_{self.room_id}"

#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )

#             await self.accept()

#             # Send last 20 messages
#             messages = await self.get_last_messages()

#             await self.send(
#                 text_data=json.dumps({
#                     "type": "chat_history",
#                     "messages": messages
#                 })
#             )

#         except Exception as e:

#             print("CONNECT ERROR:", str(e))

#     async def disconnect(self, close_code):

#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):

#         data = json.loads(text_data)

#         sender_id = data.get("sender_id")
#         message = data.get("message")

#         chat_message = await self.save_message(
#             sender_id,
#             message
#         )

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 "message": chat_message.message,
#                 "sender_id": sender_id,
#                 "message_id": chat_message.id,
#                 "created_at": str(chat_message.created_at)
#             }
#         )

#     async def chat_message(self, event):

#         await self.send(
#             text_data=json.dumps({
#                 "message_id": event["message_id"],
#                 "sender_id": event["sender_id"],
#                 "message": event["message"],
#                 "created_at": event["created_at"]
#             })
#         )

#     @database_sync_to_async
#     def save_message(self, sender_id, message):

#         room = ChatRoom.objects.get(
#             id=self.room_id
#         )

#         sender = UserRegisterdb.objects.get(
#             id=sender_id
#         )

#         return ChatMessage.objects.create(
#             room=room,
#             sender=sender,
#             message=message
#         )
        
#     @database_sync_to_async
#     def get_last_messages(self):

#         messages = (
#             ChatMessage.objects
#             .filter(room_id=self.room_id)
#             .select_related("sender")
#             .order_by("-created_at")[:20]
#         )

#         data = []

#         for msg in reversed(messages):

#             data.append({
#                 "message_id": msg.id,
#                 "sender_id": msg.sender.id,
#                 "sender_name": msg.sender.nick_name,
#                 "message": msg.message,
#                 "created_at": str(msg.created_at),
#             })

#         return data



