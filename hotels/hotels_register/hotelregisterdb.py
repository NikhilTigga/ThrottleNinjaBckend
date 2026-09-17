from django.db import models


class HotelVendor(models.Model):

    vendor_name = models.CharField(
        max_length=255
    )

    mobile_no = models.CharField(
        max_length=15,
        unique=True
    )

    password = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True
    )

    aadhar_card = models.CharField(
        max_length=20,
        unique=True
    )

    pan_card = models.CharField(
        max_length=20,
        unique=True
    )

    # Bank Details
    account_holder_name = models.CharField(
        max_length=255
    )

    bank_name = models.CharField(
        max_length=255
    )

    account_number = models.CharField(
        max_length=50
    )

    ifsc_code = models.CharField(
        max_length=20
    )

    branch_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # Optional Document Uploads
    aadhar_image = models.ImageField(
        upload_to="hotel_vendor/aadhar/",
        null=True,
        blank=True
    )

    pan_image = models.ImageField(
        upload_to="hotel_vendor/pan/",
        null=True,
        blank=True
    )

    bank_passbook_image = models.ImageField(
        upload_to="hotel_vendor/bank/",
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.vendor_name
    


class Hotel(models.Model):

    vendor = models.ForeignKey(
        "HotelVendor",
        on_delete=models.CASCADE,
        related_name="hotels"
    )

    name = models.CharField(
        max_length=255
    )
    
    # Multiple Images
    images = models.JSONField(
        default=list,
        blank=True,
        help_text="Store multiple hotel image URLs"
    )

    address = models.TextField()

    # Location (Optional)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    # Categorized Amenities
    amenities = models.JSONField(
        default=dict,
        blank=True,
        help_text="Store amenities category-wise"
    )

    # Property Rules and Information
    property_rules_info = models.TextField(
        null=True,
        blank=True
    )

    # Approval Status
    APPROVAL_STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS,
        default="pending"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name
    
    

class HotelRoom(models.Model):

    hotel = models.ForeignKey(
        "Hotel",
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_name = models.CharField(
        max_length=255
    )

    adults_qty = models.PositiveIntegerField(
        default=1
    )

    room_images = models.JSONField(
        default=list,
        blank=True
    )

    # Room Features
    room_features = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        {
            "sq_ft": "250",
            "view": "City View",
            "bed": "King Bed",
            "bathroom": "Private Bathroom"
        }
        """
    )

    # Room Amenities
    amenities = models.JSONField(
        default=dict,
        blank=True
    )

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_rooms = models.PositiveIntegerField(
        default=1
    )

    available_rooms = models.PositiveIntegerField(
        default=1
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.hotel.name} - {self.room_name}"
    
    


class RoomPriceCart(models.Model):

    room = models.ForeignKey(
        "HotelRoom",
        on_delete=models.CASCADE,
        related_name="price_carts"
    )

    # Cart / Plan Name
    cart_name = models.CharField(
        max_length=255
    )

    # Room Facilities
    room_facilities = models.JSONField(
        default=dict,
        blank=True
    )

    
    # Base Room Price
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Discount
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # GST Percentage
    gst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.room.room_name} - {self.cart_name}"
    
    
class HotelReview(models.Model):

    hotel = models.ForeignKey(
        "Hotel",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        "myapp.UserRegisterdb",
        on_delete=models.CASCADE,
        related_name="hotel_reviews"
    )

    # Overall Rating
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        help_text="Rating from 1.0 to 5.0"
    )

    # Category-wise Ratings
    cleanliness_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )

    location_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )

    service_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )

    value_for_money_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )

    facilities_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )

    # Review
    review_title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    review = models.TextField(
        null=True,
        blank=True
    )

    # Review Images
    images = models.JSONField(
        default=list,
        blank=True
    )

    # Hotel Booking Reference
    booking_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    is_verified_stay = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.hotel.name} - {self.rating} - {self.user.full_name}"