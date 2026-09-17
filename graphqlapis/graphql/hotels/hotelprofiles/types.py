import strawberry
from typing import Optional, List
from strawberry.scalars import JSON


@strawberry.type
class HotelVendorType:
    id: int
    vendor_name: str
    mobile_no: str
    email: Optional[str]

    account_holder_name: str
    bank_name: str
    account_number: str
    ifsc_code: str
    branch_name: Optional[str]

    aadhar_card: str
    pan_card: str

    aadhar_image: Optional[str]
    pan_image: Optional[str]
    bank_passbook_image: Optional[str]

    is_active: bool


@strawberry.type
class HotelType:
    id: int
    name: str
    address: str

    images: List[str]

    latitude: Optional[float]
    longitude: Optional[float]

    amenities: JSON
    property_rules_info: Optional[str]

    approval_status: str
    is_active: bool


@strawberry.type
class HotelProfileType:
    vendor: HotelVendorType
    hotel: HotelType