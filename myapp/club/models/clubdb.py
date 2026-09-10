from django.db import models

class Club(models.Model):
    
    VISIBILITY = [
        ('public', 'Public'),
        ('private','Private')
    ]

    name = models.CharField(max_length=255)
    
    club_img = models.ImageField(upload_to='club_img', null=True, blank=True)
    club_address = models.TextField(null=True , blank=True)
    
    club_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    club_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    

    description = models.TextField(blank=True)

    club_image = models.ImageField(
        upload_to="clubs/",
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        "myapp.UserRegisterdb",
        on_delete=models.CASCADE,
        related_name="created_clubs"
    )
    
    visibility = models.CharField(
    max_length=10,
    choices=VISIBILITY,
    default="public"
    )
    
    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    




class ClubMember(models.Model):

    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        "myapp.UserRegisterdb",
        on_delete=models.CASCADE
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("club", "user")
        
        

class ClubMessage(models.Model):

    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        "myapp.UserRegisterdb",
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message[:50]
    


class ClubJoinRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name="join_requests"
    )

    user = models.ForeignKey(
        "myapp.UserRegisterdb",
        on_delete=models.CASCADE,
        related_name="club_join_requests"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("club", "user")