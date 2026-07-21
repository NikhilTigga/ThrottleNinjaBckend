from django.db import models
from django.utils import timezone


class UserRegisterdb(models.Model):
    full_name = models.CharField(max_length=200,)
    nick_name = models.CharField(max_length= 200, unique=True)
    mobileno = models.CharField(max_length=15 , unique=True)
    city = models.CharField(max_length=100 )
    password = models.CharField(max_length =200 , null=True , blank=True)
    profile_img = models.URLField(max_length=1000, null=True, blank=True)
    profile_img_fileid = models.CharField(max_length=200 , null = True ,blank =True)
    bike_image = models.URLField(max_length=1000, null=True, blank=True)
    bike_image_fileid = models.CharField(max_length=200 , null = True, blank=True)
    bike_brand_name = models.CharField(max_length=200 , null=True, blank=True)
    bike_model = models.CharField(max_length=200 , null=True , )
    manufacturing_year = models.DateField(null=True , blank=True)
    vehichle_no = models.CharField(max_length=200 , null=True , blank=True)
    fcm_token = models.CharField(max_length = 200 , null= True , blank=True)
    
    is_private = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    last_seen = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )

    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = "users"

        indexes = [
            models.Index(fields=["nick_name"]),
            models.Index(fields=["mobileno"]),
            models.Index(fields=["last_seen"]),
        ]
    def __str__(self):
        return self.nick_name
