from django.db import models
from django.utils import timezone
from myapp.account.models.user import UserRegisterdb

class UserBlock(models.Model):
    blocker = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="blocked_users"
    )

    blocked = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="blocked_by_users"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_blocks"

        constraints = [
            models.UniqueConstraint(
                fields=["blocker", "blocked"],
                name="unique_block_relation"
            )
        ]