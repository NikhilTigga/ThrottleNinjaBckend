from django.db import models
from django.utils import timezone
from myapp.account.models import UserRegisterdb
from myapp.posts.models.post import Post




class Userfeed(models.Model):

    user = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="feed_items"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="feed_entries"
    )

    creator = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="created_feed_entries"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
      

        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_feed_post"
            )
        ]

        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["post"]),
            models.Index(fields=["creator"]),
        ]

    def __str__(self):
        return f"Feed User: {self.user_id} -> Post: {self.post_id}"