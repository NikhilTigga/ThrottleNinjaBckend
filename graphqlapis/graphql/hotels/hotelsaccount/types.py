import strawberry
from strawberry.scalars import JSON


@strawberry.input
class HotelVendorInput:
    vendor_name: str
    mobile_no: str
    password: str
    aadhar_card: str
    pan_card: str
    account_holder_name: str
    bank_name: str
    account_number: str
    ifsc_code: str
    email: str | None = None
    branch_name: str | None = None


@strawberry.input
class HotelInput:
    name: str
    address: str
    images: list[str] | None = None
    latitude: float | None = None
    longitude: float | None = None
    amenities: JSON | None = None
    property_rules_info: str | None = None


@strawberry.type
class HotelRegistrationResponse:
    status: int
    message: str
    vendor_id: int | None = None
    hotel_id: int | None = None


@strawberry.type
class HotelVendorLoginResponse:
    status: int
    message: str
    access_token: str | None = None
    refresh_token: str | None = None
    vendor_id: int | None = None
    hotel_id: int | None = None