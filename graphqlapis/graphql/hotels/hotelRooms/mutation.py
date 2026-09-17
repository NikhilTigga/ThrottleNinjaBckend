from decimal import Decimal

from django.db import transaction
import strawberry
from strawberry.types import Info

from hotels.models import Hotel, HotelRoom, RoomPriceCart
from imageKit.imagekit_config import imagekit

from .types import CreateHotelRoomResponse, HotelRoomInput, HotelRoomType
from .types import RoomPriceCartInput, RoomPriceCartType


def upload_room_images(images):
    uploaded_images = []

    for image in images or []:
        uploaded_file = getattr(image, "file", image)
        file_name = getattr(
            image,
            "filename",
            getattr(uploaded_file, "name", "hotel-room-image"),
        )
        result = imagekit.files.upload(
            file=uploaded_file.read(),
            file_name=file_name,
            use_unique_file_name=True,
            folder="/hotels/rooms",
        )
        uploaded_images.append(result.url)

    return uploaded_images


def room_type(room):
    return HotelRoomType(
        id=room.id,
        hotel_id=room.hotel_id,
        room_name=room.room_name,
        adults_qty=room.adults_qty,
        room_images=room.room_images or [],
        room_features=room.room_features or {},
        amenities=room.amenities or {},
        price_per_night=float(room.price_per_night),
        discounted_price=(
            float(room.discounted_price)
            if room.discounted_price is not None
            else None
        ),
        total_rooms=room.total_rooms,
        available_rooms=room.available_rooms,
        is_active=room.is_active,
        price_carts=[
            RoomPriceCartType(
                id=price_cart.id,
                cart_name=price_cart.cart_name,
                room_facilities=price_cart.room_facilities or {},
                base_price=float(price_cart.base_price),
                discount=float(price_cart.discount),
                gst=float(price_cart.gst),
                is_active=price_cart.is_active,
            )
            for price_cart in room.price_carts.all()
        ],
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_hotel_room(
        self,
        info: Info,
        hotel_id: int,
        room_data: HotelRoomInput,
    ) -> CreateHotelRoomResponse:
        vendor = info.context.request.hotel_vendor
        if vendor is None:
            return CreateHotelRoomResponse(
                status=0,
                message="Hotel vendor authentication required",
            )

        hotel = Hotel.objects.filter(id=hotel_id, vendor=vendor).first()
        if hotel is None:
            return CreateHotelRoomResponse(
                status=0,
                message="Hotel not found or not owned by this vendor",
            )

        if room_data.adults_qty < 1:
            return CreateHotelRoomResponse(
                status=0,
                message="adults_qty must be at least 1",
            )

        if room_data.total_rooms < 1:
            return CreateHotelRoomResponse(
                status=0,
                message="total_rooms must be at least 1",
            )

        available_rooms = (
            room_data.available_rooms
            if room_data.available_rooms is not None
            else room_data.total_rooms
        )
        if available_rooms < 0 or available_rooms > room_data.total_rooms:
            return CreateHotelRoomResponse(
                status=0,
                message="available_rooms must be between 0 and total_rooms",
            )

        if room_data.price_per_night < 0:
            return CreateHotelRoomResponse(
                status=0,
                message="price_per_night cannot be negative",
            )

        if (
            room_data.discounted_price is not None
            and (
                room_data.discounted_price < 0
                or room_data.discounted_price > room_data.price_per_night
            )
        ):
            return CreateHotelRoomResponse(
                status=0,
                message="discounted_price must be between 0 and price_per_night",
            )

        for price_cart in room_data.price_carts or []:
            if price_cart.base_price < 0:
                return CreateHotelRoomResponse(
                    status=0,
                    message="cart base_price cannot be negative",
                )
            if price_cart.discount < 0:
                return CreateHotelRoomResponse(
                    status=0,
                    message="cart discount cannot be negative",
                )
            if price_cart.gst < 0:
                return CreateHotelRoomResponse(
                    status=0,
                    message="cart gst cannot be negative",
                )

        try:
            with transaction.atomic():
                room = HotelRoom.objects.create(
                    hotel=hotel,
                    room_name=room_data.room_name,
                    adults_qty=room_data.adults_qty,
                    room_images=upload_room_images(room_data.room_images),
                    room_features=room_data.room_features or {},
                    amenities=room_data.amenities or {},
                    price_per_night=Decimal(str(room_data.price_per_night)),
                    discounted_price=(
                        Decimal(str(room_data.discounted_price))
                        if room_data.discounted_price is not None
                        else None
                    ),
                    total_rooms=room_data.total_rooms,
                    available_rooms=available_rooms,
                    is_active=room_data.is_active,
                )
                RoomPriceCart.objects.bulk_create([
                    RoomPriceCart(
                        room=room,
                        cart_name=price_cart.cart_name,
                        room_facilities=price_cart.room_facilities or {},
                        base_price=Decimal(str(price_cart.base_price)),
                        discount=Decimal(str(price_cart.discount)),
                        gst=Decimal(str(price_cart.gst)),
                        is_active=price_cart.is_active,
                    )
                    for price_cart in room_data.price_carts or []
                ])
        except Exception as error:
            return CreateHotelRoomResponse(status=0, message=str(error))

        return CreateHotelRoomResponse(
            status=1,
            message="Hotel room created successfully",
            room=room_type(room),
        )
