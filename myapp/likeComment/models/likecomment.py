from django.db import models
from django.utils import timezone
from myapp.account.models import UserRegisterdb
from myapp.posts.models.post import Post


class Like(models.Model):
    user = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        
        
class Comment(models.Model):
    user = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user} - {self.post_id}"
