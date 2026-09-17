from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import check_password, make_password
import strawberry

from hotels.models import Hotel, HotelVendor
from jwt_utils import generate_hotel_vendor_jwt_token, generate_hotel_vendor_refresh_token

from .types import (
    HotelInput,
    HotelRegistrationResponse,
    HotelVendorInput,
    HotelVendorLoginResponse,
)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register_hotel(
        self,
        vendor: HotelVendorInput,
        hotel: HotelInput,
    ) -> HotelRegistrationResponse:
        try:
            with transaction.atomic():
                hotel_vendor = HotelVendor.objects.create(
                    vendor_name=vendor.vendor_name,
                    mobile_no=vendor.mobile_no,
                    password=make_password(vendor.password),
                    email=vendor.email,
                    aadhar_card=vendor.aadhar_card,
                    pan_card=vendor.pan_card,
                    account_holder_name=vendor.account_holder_name,
                    bank_name=vendor.bank_name,
                    account_number=vendor.account_number,
                    ifsc_code=vendor.ifsc_code,
                    branch_name=vendor.branch_name,
                )
                registered_hotel = Hotel.objects.create(
                    vendor=hotel_vendor,
                    name=hotel.name,
                    address=hotel.address,
                    images=hotel.images or [],
                    latitude=hotel.latitude,
                    longitude=hotel.longitude,
                    amenities=hotel.amenities or {},
                    property_rules_info=hotel.property_rules_info,
                )
        except IntegrityError:
            return HotelRegistrationResponse(
                status=0,
                message="A vendor with the same mobile number, email, Aadhar card, or PAN card already exists",
            )

        return HotelRegistrationResponse(
            status=1,
            message="Hotel registered successfully",
            vendor_id=hotel_vendor.id,
            hotel_id=registered_hotel.id,
        )

    @strawberry.mutation
    def hotel_vendor_login(
        self,
        mobile_no: str,
        password: str,
    ) -> HotelVendorLoginResponse:
        try:
            vendor = HotelVendor.objects.get(mobile_no=mobile_no)
        except HotelVendor.DoesNotExist:
            return HotelVendorLoginResponse(
                status=0,
                message="Vendor not found",
            )

        if not vendor.is_active or not check_password(password, vendor.password):
            return HotelVendorLoginResponse(
                status=0,
                message="Invalid password or inactive vendor",
            )

        hotel = vendor.hotels.order_by("id").first()

        return HotelVendorLoginResponse(
            status=1,
            message="Login successful",
            access_token=generate_hotel_vendor_jwt_token(vendor),
            refresh_token=generate_hotel_vendor_refresh_token(vendor),
            vendor_id=vendor.id,
            hotel_id=hotel.id if hotel else None,
        )