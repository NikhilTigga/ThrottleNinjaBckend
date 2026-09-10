import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from myapp.models import Club , ClubMessage, ClubMember
from myapp.models import UserRegisterdb



class ClubConsumer(AsyncWebsocketConsumer):

    # ==========================================
    # CONNECT
    # ==========================================

    async def connect(self):

        self.club_id = self.scope["url_route"]["kwargs"]["club_id"]

        self.room_group_name = f"club_{self.club_id}"

        # --------------------------------------
        # Check club exists
        # --------------------------------------

        club_exists = await self.club_exists()

        if not club_exists:
            await self.close()
            return

        # --------------------------------------
        # Add websocket to club group
        # --------------------------------------

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # --------------------------------------
        # Send latest 20 messages
        # --------------------------------------

        messages = await self.get_last_messages()

        await self.send(
            text_data=json.dumps({
                "type": "club_history",
                "messages": messages
            })
        )

    # ==========================================
    # DISCONNECT
    # ==========================================

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # ==========================================
    # RECEIVE
    # ==========================================

    async def receive(self, text_data):

        try:

            data = json.loads(text_data)

            event_type = data.get("type")

            # ==================================
            # SEND MESSAGE
            # ==================================

            if event_type == "message":

                sender_id = data.get("sender_id")
                message = data.get("message")

                if not sender_id or not message:

                    await self.send(
                        text_data=json.dumps({
                            "type": "error",
                            "message": "sender_id and message are required"
                        })
                    )

                    return

                # --------------------------------
                # Check club membership
                # --------------------------------

                is_member = await self.check_member(
                    sender_id
                )

                if not is_member:

                    await self.send(
                        text_data=json.dumps({
                            "type": "error",
                            "message": "You are not a member of this club"
                        })
                    )

                    return

                # --------------------------------
                # Save message
                # --------------------------------

                club_message = await self.save_message(
                    sender_id,
                    message
                )

                # --------------------------------
                # Broadcast message
                # --------------------------------

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "club_message",
                        "message_id": club_message.id,
                        "sender_id": club_message.sender.id,
                        "sender_name": club_message.sender.nick_name,
                        "message": club_message.message,
                        "is_read": club_message.is_read,
                        "created_at": str(
                            club_message.created_at
                        )
                    }
                )

            # ==================================
            # TYPING
            # ==================================

            elif event_type == "typing":

                sender_id = data.get("sender_id")

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "typing_event",
                        "sender_id": sender_id
                    }
                )

            # ==================================
            # STOP TYPING
            # ==================================

            elif event_type == "stop_typing":

                sender_id = data.get("sender_id")

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "stop_typing_event",
                        "sender_id": sender_id
                    }
                )

            # ==================================
            # MESSAGE SEEN
            # ==================================

            elif event_type == "seen":

                message_id = data.get("message_id")
                sender_id = data.get("sender_id")

                if not message_id:
                    return

                # --------------------------------
                # Mark message as read
                # --------------------------------

                await self.mark_message_seen(
                    message_id,
                    sender_id
                )

                # --------------------------------
                # Broadcast seen event
                # --------------------------------

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "message_seen",
                        "message_id": message_id,
                        "sender_id": sender_id
                    }
                )

        except json.JSONDecodeError:

            await self.send(
                text_data=json.dumps({
                    "type": "error",
                    "message": "Invalid JSON"
                })
            )

        except Exception as e:

            await self.send(
                text_data=json.dumps({
                    "type": "error",
                    "message": str(e)
                })
            )

    # ==========================================
    # CLUB MESSAGE
    # ==========================================

    async def club_message(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "message",
                "message_id": event["message_id"],
                "sender_id": event["sender_id"],
                "sender_name": event["sender_name"],
                "message": event["message"],
                "is_read": event["is_read"],
                "created_at": event["created_at"]
            })
        )

    # ==========================================
    # TYPING
    # ==========================================

    async def typing_event(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "typing",
                "sender_id": event["sender_id"]
            })
        )

    # ==========================================
    # STOP TYPING
    # ==========================================

    async def stop_typing_event(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "stop_typing",
                "sender_id": event["sender_id"]
            })
        )

    # ==========================================
    # MESSAGE SEEN
    # ==========================================

    async def message_seen(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "seen",
                "message_id": event["message_id"],
                "sender_id": event["sender_id"]
            })
        )

    # ==========================================
    # CHECK CLUB EXISTS
    # ==========================================

    @database_sync_to_async
    def club_exists(self):

        return Club.objects.filter(
            id=self.club_id
        ).exists()

    # ==========================================
    # CHECK MEMBER
    # ==========================================

    @database_sync_to_async
    def check_member(self, user_id):

        return ClubMember.objects.filter(
            club_id=self.club_id,
            user_id=user_id
        ).exists()

    # ==========================================
    # SAVE MESSAGE
    # ==========================================

    @database_sync_to_async
    def save_message(self, sender_id, message):

        club = Club.objects.get(
            id=self.club_id
        )

        sender = UserRegisterdb.objects.get(
            id=sender_id
        )

        return ClubMessage.objects.create(
            club=club,
            sender=sender,
            message=message
        )

    # ==========================================
    # MARK MESSAGE SEEN
    # ==========================================

    @database_sync_to_async
    def mark_message_seen(self, message_id, user_id):

        ClubMessage.objects.filter(
            id=message_id,
            club_id=self.club_id
        ).update(
            is_read=True
        )

    # ==========================================
    # LAST 20 MESSAGES
    # ==========================================

    @database_sync_to_async
    def get_last_messages(self):

        messages = (
            ClubMessage.objects
            .filter(
                club_id=self.club_id
            )
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
                "message": msg.message,
                "created_at": str(
                    msg.created_at
                )
            })

        return data