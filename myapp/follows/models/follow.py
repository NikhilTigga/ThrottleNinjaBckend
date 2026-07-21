from django.db import models
from django.utils import timezone
from myapp.account.models.user import UserRegisterdb
class Follow(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"

    follower = models.ForeignKey(
       UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACCEPTED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_follows"

        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow_relation"
            )
        ]

        indexes = [
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]
        