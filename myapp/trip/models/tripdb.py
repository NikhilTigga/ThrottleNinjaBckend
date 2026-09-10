from django.db import models
from myapp.models import UserRegisterdb, Club


class Trip(models.Model):

    # ==========================================
    # GROUP / SOLO
    # ==========================================

    TRIP_MODE_CHOICES = [
        ("group", "Group Trip"),
        ("solo", "Solo Trip"),
    ]

    trip_mode = models.CharField(
        max_length=10,
        choices=TRIP_MODE_CHOICES,
        default="group"
    )

    # ==========================================
    # BASIC INFORMATION
    # ==========================================

    trip_name = models.CharField(
        max_length=255
    )

    trip_photo = models.ImageField(
        upload_to="trips/",
        null=True,
        blank=True
    )

    trip_note = models.TextField(
        null=True,
        blank=True
    )

    # ==========================================
    # DESTINATION
    # ==========================================

    destination_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    destination_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    destination_address = models.TextField(
        null=True,
        blank=True
    )

    # ==========================================
    # MEET-UP POINT
    # ==========================================

    meetup_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    meetup_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    meetup_address = models.TextField(
        null=True,
        blank=True
    )

    meetup_time = models.TimeField(
        null=True,
        blank=True
    )

    # ==========================================
    # CLUB
    # ==========================================

    trip_associated_with_club = models.BooleanField(
        default=False
    )

    club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trips"
    )

    # ==========================================
    # ROUND TRIP
    # ==========================================

    is_round_trip = models.BooleanField(
        default=False
    )

    # ==========================================
    # DURATION
    # ==========================================

    trip_duration_days = models.PositiveIntegerField(
        default=1
    )

    # ==========================================
    # DATE
    # ==========================================

    start_date = models.DateField()

    # ==========================================
    # TRIP PAYMENT TYPE
    # ==========================================

    PAYMENT_TYPE_CHOICES = [
        ("free", "Free"),
        ("split", "Split"),
        ("paid", "Paid"),
    ]

    trip_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES,
        default="free"
    )

    # ==========================================
    # TRIP COST PER PERSON
    # ==========================================

    trip_cost_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # ==========================================
    # TRIP VISIBILITY
    # ==========================================

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default="public"
    )

    # ==========================================
    # CREATED BY
    # ==========================================

    created_by = models.ForeignKey(
        UserRegisterdb,
        on_delete=models.CASCADE,
        related_name="created_trips"
    )

    # ==========================================
    # POLICIES
    # ==========================================

    cancellation_policy = models.TextField(
        null=True,
        blank=True
    )

    terms_and_conditions = models.TextField(
        null=True,
        blank=True
    )
    
    included_feature = models.JSONField( # Feature Name 
    default=list,
    blank=True
    )
    
    payment_mode_split_include = models.JSONField( # Feature Name
        default=list, 
        blank=True
        )

    # ==========================================
    # CREATED AT
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.trip_name
    
    


class TripDay(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="days"
    )

    day_number = models.PositiveIntegerField()

    # ==========================================
    # START LOCATION
    # ==========================================

    start_location_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    start_location_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    start_location_address = models.TextField(
        null=True,
        blank=True
    )

    # ==========================================
    # STOP LOCATION
    # ==========================================

    stop_location_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    stop_location_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    stop_location_address = models.TextField(
        null=True,
        blank=True
    )

    # ==========================================
    # END LOCATION
    # ==========================================

    end_location_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    end_location_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    end_location_address = models.TextField(
        null=True,
        blank=True
    )

    # ==========================================
    # FLAG OFF
    # ==========================================

    flag_off_time = models.TimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["day_number"]

        unique_together = (
            "trip",
            "day_number"
        )

    def __str__(self):
        return f"{self.trip.trip_name} - Day {self.day_number}"