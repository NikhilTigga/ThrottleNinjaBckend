from django.db import models

from account.models import UserRegisterdb

class ChatRoom(models.Model):

    users = models.ManyToManyField(
        UserRegisterdb,
        related_name="chat_rooms"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_ids = self.users.values_list(
            "id",
            flat=True
        )
        return f"Room {'-'.join(map(str, user_ids))}"


