

import strawberry
from typing import Optional, List
from strawberry.file_uploads import Upload

@strawberry.input
class EditHotelVendorInput:
    vendor_name: Optional[str] = None
    email: Optional[str] = None
    account_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    branch_name: Optional[str] = None


@strawberry.input
class EditHotelInput:
    name: Optional[str] = None
    address: Optional[str] = None
    images: Optional[List[Upload]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    amenities: Optional[strawberry.scalars.JSON] = None
    property_rules_info: Optional[str] = None


@strawberry.type
class EditHotelProfileResponse:
    status: int
    message: str