from django.db import transaction
import strawberry
from strawberry.types import Info

from hotels.models import HotelVendor, Hotel
from imageKit.imagekit_config import imagekit
from .types import (
    EditHotelVendorInput,
    EditHotelInput,
    EditHotelProfileResponse,
)


@strawberry.type
class Mutation:

    @strawberry.mutation
    def edit_hotel_profile(
        self,
        info: Info,
        vendor_data: EditHotelVendorInput,
        hotel_data: EditHotelInput,
        vendor_id: int | None = None,
    ) -> EditHotelProfileResponse:

        vendor = info.context.request.hotel_vendor
        if vendor is None and vendor_id is not None:
            vendor = HotelVendor.objects.filter(id=vendor_id).first()

        if vendor is None:
            return EditHotelProfileResponse(
                status=0,
                message="Hotel vendor authentication required"
            )

        try:
            hotel = Hotel.objects.get(vendor=vendor)

        except Hotel.DoesNotExist:
            return EditHotelProfileResponse(
                status=0,
                message="Hotel not found"
            )

        try:
            with transaction.atomic():

                # ==========================
                # UPDATE VENDOR DETAILS
                # ==========================

                if vendor_data.vendor_name is not None:
                    vendor.vendor_name = vendor_data.vendor_name

                if vendor_data.email is not None:
                    vendor.email = vendor_data.email

                if vendor_data.account_holder_name is not None:
                    vendor.account_holder_name = vendor_data.account_holder_name

                if vendor_data.bank_name is not None:
                    vendor.bank_name = vendor_data.bank_name

                if vendor_data.account_number is not None:
                    vendor.account_number = vendor_data.account_number

                if vendor_data.ifsc_code is not None:
                    vendor.ifsc_code = vendor_data.ifsc_code

                if vendor_data.branch_name is not None:
                    vendor.branch_name = vendor_data.branch_name

                vendor.save()

                # ==========================
                # UPDATE HOTEL DETAILS
                # ==========================

                if hotel_data.name is not None:
                    hotel.name = hotel_data.name

                if hotel_data.address is not None:
                    hotel.address = hotel_data.address

                if hotel_data.images is not None:
                    uploaded_images = []

                    for image in hotel_data.images:
                        uploaded_file = getattr(image, "file", image)
                        file_name = getattr(
                            image,
                            "filename",
                            getattr(uploaded_file, "name", "hotel-image"),
                        )
                        result = imagekit.files.upload(
                            file=uploaded_file.read(),
                            file_name=file_name,
                            use_unique_file_name=True,
                            folder="/hotels/images",
                        )
                        uploaded_images.append(result.url)

                    hotel.images = uploaded_images

                if hotel_data.latitude is not None:
                    hotel.latitude = hotel_data.latitude

                if hotel_data.longitude is not None:
                    hotel.longitude = hotel_data.longitude

                if hotel_data.amenities is not None:
                    hotel.amenities = hotel_data.amenities

                if hotel_data.property_rules_info is not None:
                    hotel.property_rules_info = hotel_data.property_rules_info

                hotel.save()

                return EditHotelProfileResponse(
                    status=1,
                    message="Hotel profile updated successfully"
                )

        except Exception as e:
            return EditHotelProfileResponse(
                status=0,
                message=str(e)
            )