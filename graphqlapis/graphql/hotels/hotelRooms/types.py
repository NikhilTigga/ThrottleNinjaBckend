from typing import Optional

import strawberry
from strawberry.file_uploads import Upload
from strawberry.scalars import JSON


@strawberry.input
class HotelRoomInput:
    room_name: str
    adults_qty: int = 1
    room_images: Optional[list[Upload]] = None
    room_features: Optional[JSON] = None
    amenities: Optional[JSON] = None
    price_per_night: float = 0
    discounted_price: Optional[float] = None
    total_rooms: int = 1
    available_rooms: Optional[int] = None
    is_active: bool = True
    price_carts: Optional[list["RoomPriceCartInput"]] = None


@strawberry.input
class RoomPriceCartInput:
    cart_name: str
    room_facilities: Optional[JSON] = None
    base_price: float
    discount: float = 0
    gst: float = 0
    is_active: bool = True
    id: Optional[int] = None


@strawberry.type(name="HotelRoomPriceCartType")
class RoomPriceCartType:
    id: int
    cart_name: str
    room_facilities: JSON
    base_price: float
    discount: float
    gst: float
    is_active: bool


@strawberry.type
class HotelRoomType:
    id: int
    hotel_id: int
    room_name: str
    adults_qty: int
    room_images: list[str]
    room_features: JSON
    amenities: JSON
    price_per_night: float
    discounted_price: Optional[float]
    total_rooms: int
    available_rooms: int
    is_active: bool
    price_carts: list[RoomPriceCartType]


@strawberry.type
class CreateHotelRoomResponse:
    status: int
    message: str
    room: Optional[HotelRoomType] = None
