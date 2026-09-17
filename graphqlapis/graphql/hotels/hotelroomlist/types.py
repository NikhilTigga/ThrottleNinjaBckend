import strawberry
from typing import List, Optional


@strawberry.type
class RoomPriceCartType:
    id: int
    cart_name: str
    room_facilities: str
    base_price: float
    discount: float
    gst: float
    is_active: bool


@strawberry.type
class HotelRoomlistType:
    id: int
    room_name: str
    adults_qty: int
    room_images: List[str]
    room_features: str
    amenities: str
    price_per_night: float
    discounted_price: Optional[float]
    total_rooms: int
    available_rooms: int
    is_active: bool


@strawberry.type
class HotelRoomDetailType:
    id: int
    room_name: str
    adults_qty: int
    room_images: List[str]
    room_features: str
    amenities: str
    price_per_night: float
    discounted_price: Optional[float]
    total_rooms: int
    available_rooms: int
    is_active: bool
    price_carts: List[RoomPriceCartType]


@strawberry.type
class HotelRoomListResponse:
    status: int
    message: str
    rooms: List[HotelRoomlistType]


@strawberry.type
class HotelRoomDetailResponse:
    status: int
    message: str
    room: Optional[HotelRoomDetailType]