from hotels.models import Hotel, HotelVendor

from .types import *

import strawberry
from strawberry.types import Info

@strawberry.type
class Query:

    @strawberry.field
    def hotel_profile(
        self,
        info: Info,
        hotel_id: int
    ) -> Optional[HotelProfileType]:
        # Get logged-in hotel vendor
        vendor = info.context.request.hotel_vendor
        # Authentication check
        if not vendor:
            raise Exception("Hotel vendor authentication required") 

        try:
            hotel = Hotel.objects.select_related(
                "vendor"
            ).get(
                id=hotel_id
            )
            vendor = hotel.vendor
            return HotelProfileType(
                vendor=HotelVendorType(
                    id=vendor.id,
                    vendor_name=vendor.vendor_name,
                    mobile_no=vendor.mobile_no,
                    email=vendor.email,
                    account_holder_name=vendor.account_holder_name,
                    bank_name=vendor.bank_name,
                    account_number=vendor.account_number,
                    ifsc_code=vendor.ifsc_code,
                    branch_name=vendor.branch_name,
                    aadhar_card=vendor.aadhar_card,
                    pan_card=vendor.pan_card,
                    aadhar_image=vendor.aadhar_image.url if vendor.aadhar_image else None,
                    pan_image=vendor.pan_image.url if vendor.pan_image else None,
                    bank_passbook_image=vendor.bank_passbook_image.url if vendor.bank_passbook_image else None,
                    is_active=vendor.is_active,
                ),

                hotel=HotelType(
                    id=hotel.id,
                    name=hotel.name,
                    address=hotel.address,

                    images=hotel.images or [],

                    latitude=float(hotel.latitude) if hotel.latitude else None,
                    longitude=float(hotel.longitude) if hotel.longitude else None,

                    amenities=hotel.amenities,
                    property_rules_info=hotel.property_rules_info,

                    approval_status=hotel.approval_status,
                    is_active=hotel.is_active,
                )
            )
        except Hotel.DoesNotExist:
            return None