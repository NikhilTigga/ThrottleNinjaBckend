from django.db import models
from django.utils import timezone
from myapp.account.models import UserRegisterdb 
from myapp.hashtag.models import Hashtag


class Post(models.Model):
    creator = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    caption = models.TextField(
        null=True,
        blank=True
    )
    
    hashtags = models.ManyToManyField(
        Hashtag,
        blank=True,
        related_name="posts"
    )
    
    location = models.CharField(max_length=100 , null = True , blank=True)

    like_count = models.PositiveIntegerField(default=0)

    comment_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.creator.name} - {self.id}"


class PostMedia(models.Model):

    MEDIA_TYPE = (
        ("image", "Image"),
        ("video", "Video"),
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="media"
    )

    media_url = models.URLField()

    media_id = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPE
    )
    
    thumbnail_url = models.URLField(
        null=True,
        blank=True
    )
    
    media_thumbnail_id = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.media_type} - {self.post.id}"
