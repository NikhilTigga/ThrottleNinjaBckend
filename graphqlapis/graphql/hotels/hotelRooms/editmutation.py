from decimal import Decimal

import strawberry
from django.db import transaction
from strawberry.types import Info

from hotels.models import Hotel, HotelRoom, RoomPriceCart
from imageKit.imagekit_config import imagekit

from .types import (
    HotelRoomInput,
    HotelRoomType,
    RoomPriceCartType,
    CreateHotelRoomResponse,
)


# =========================================================
# UPLOAD ROOM IMAGES
# =========================================================

def upload_room_images(images):

    uploaded_images = []

    for image in images or []:

        uploaded_file = getattr(image, "file", image)

        file_name = getattr(
            image,
            "filename",
            getattr(
                uploaded_file,
                "name",
                "hotel-room-image"
            ),
        )

        result = imagekit.files.upload(
            file=uploaded_file.read(),
            file_name=file_name,
            use_unique_file_name=True,
            folder="/hotels/rooms",
        )

        uploaded_images.append(result.url)

    return uploaded_images


# =========================================================
# ROOM RESPONSE TYPE
# =========================================================

def room_type(room):

    return HotelRoomType(
        id=room.id,
        hotel_id=room.hotel_id,
        room_name=room.room_name,
        adults_qty=room.adults_qty,

        room_images=room.room_images or [],

        room_features=room.room_features or {},

        amenities=room.amenities or {},

        price_per_night=float(
            room.price_per_night
        ),

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
                id=cart.id,

                cart_name=cart.cart_name,

                room_facilities=(
                    cart.room_facilities or {}
                ),

                base_price=float(
                    cart.base_price
                ),

                discount=float(
                    cart.discount
                ),

                gst=float(
                    cart.gst
                ),

                is_active=cart.is_active,
            )
            for cart in room.price_carts.all()
        ],
    )


# =========================================================
# EDIT ROOM MUTATION
# =========================================================

@strawberry.type
class Mutation:

    @strawberry.mutation
    def edit_hotel_room(
        self,
        info: Info,
        room_id: int,
        room_data: HotelRoomInput,
    ) -> CreateHotelRoomResponse:

        # =====================================================
        # AUTHENTICATION
        # =====================================================

        vendor = info.context.request.hotel_vendor

        if vendor is None:

            return CreateHotelRoomResponse(
                status=0,
                message="Hotel vendor authentication required",
            )

        try:

            # =================================================
            # GET VENDOR HOTEL
            # =================================================

            hotel = Hotel.objects.filter(
                vendor=vendor
            ).first()

            if hotel is None:

                return CreateHotelRoomResponse(
                    status=0,
                    message="Hotel not found",
                )

            # =================================================
            # GET ROOM
            # IMPORTANT:
            # Room must belong to logged-in vendor's hotel
            # =================================================

            room = (
                HotelRoom.objects
                .prefetch_related("price_carts")
                .filter(
                    id=room_id,
                    hotel=hotel,
                )
                .first()
            )

            if room is None:

                return CreateHotelRoomResponse(
                    status=0,
                    message=(
                        "Room not found or "
                        "not owned by this vendor"
                    ),
                )

            # =================================================
            # VALIDATION
            # =================================================

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

            # =================================================
            # AVAILABLE ROOMS
            # =================================================

            available_rooms = (
                room_data.available_rooms
                if room_data.available_rooms is not None
                else room.available_rooms
            )

            if (
                available_rooms < 0
                or available_rooms > room_data.total_rooms
            ):

                return CreateHotelRoomResponse(
                    status=0,
                    message=(
                        "available_rooms must be between "
                        "0 and total_rooms"
                    ),
                )

            # =================================================
            # PRICE VALIDATION
            # =================================================

            if room_data.price_per_night < 0:

                return CreateHotelRoomResponse(
                    status=0,
                    message=(
                        "price_per_night cannot be negative"
                    ),
                )

            if (
                room_data.discounted_price is not None
                and (
                    room_data.discounted_price < 0
                    or room_data.discounted_price
                    > room_data.price_per_night
                )
            ):

                return CreateHotelRoomResponse(
                    status=0,
                    message=(
                        "discounted_price must be between "
                        "0 and price_per_night"
                    ),
                )

            # =================================================
            # PRICE CART VALIDATION
            # =================================================

            for cart_data in room_data.price_carts or []:

                if cart_data.base_price < 0:

                    return CreateHotelRoomResponse(
                        status=0,
                        message=(
                            "cart base_price "
                            "cannot be negative"
                        ),
                    )

                if cart_data.discount < 0:

                    return CreateHotelRoomResponse(
                        status=0,
                        message=(
                            "cart discount "
                            "cannot be negative"
                        ),
                    )

                if cart_data.gst < 0:

                    return CreateHotelRoomResponse(
                        status=0,
                        message=(
                            "cart gst "
                            "cannot be negative"
                        ),
                    )

            # =================================================
            # UPDATE ROOM
            # =================================================

            with transaction.atomic():

                room.room_name = room_data.room_name

                room.adults_qty = (
                    room_data.adults_qty
                )

                room.room_features = (
                    room_data.room_features or {}
                )

                room.amenities = (
                    room_data.amenities or {}
                )

                room.price_per_night = Decimal(
                    str(room_data.price_per_night)
                )

                room.discounted_price = (
                    Decimal(
                        str(
                            room_data.discounted_price
                        )
                    )
                    if room_data.discounted_price
                    is not None
                    else None
                )

                room.total_rooms = (
                    room_data.total_rooms
                )

                room.available_rooms = (
                    available_rooms
                )

                room.is_active = (
                    room_data.is_active
                )

                # =================================================
                # UPDATE IMAGES ONLY IF NEW IMAGES ARE SENT
                # =================================================

                if room_data.room_images:

                    new_images = upload_room_images(
                        room_data.room_images
                    )

                    room.room_images = new_images

                room.save()

                # =================================================
                # PRICE CARTS
                # =================================================

                for cart_data in (
                    room_data.price_carts or []
                ):

                    # ---------------------------------------------
                    # EXISTING CART
                    # ---------------------------------------------

                    if cart_data.id:

                        cart = (
                            RoomPriceCart.objects.filter(
                                id=cart_data.id,
                                room=room,
                            ).first()
                        )

                        if cart:

                            cart.cart_name = (
                                cart_data.cart_name
                            )

                            cart.room_facilities = (
                                cart_data.room_facilities
                                or {}
                            )

                            cart.base_price = Decimal(
                                str(
                                    cart_data.base_price
                                )
                            )

                            cart.discount = Decimal(
                                str(
                                    cart_data.discount
                                )
                            )

                            cart.gst = Decimal(
                                str(
                                    cart_data.gst
                                )
                            )

                            cart.is_active = (
                                cart_data.is_active
                            )

                            cart.save()

                        else:

                            # -------------------------------------
                            # ID DOES NOT BELONG TO THIS ROOM
                            # CREATE NEW CART
                            # -------------------------------------

                            RoomPriceCart.objects.create(

                                room=room,

                                cart_name=(
                                    cart_data.cart_name
                                ),

                                room_facilities=(
                                    cart_data.room_facilities
                                    or {}
                                ),

                                base_price=Decimal(
                                    str(
                                        cart_data.base_price
                                    )
                                ),

                                discount=Decimal(
                                    str(
                                        cart_data.discount
                                    )
                                ),

                                gst=Decimal(
                                    str(
                                        cart_data.gst
                                    )
                                ),

                                is_active=(
                                    cart_data.is_active
                                ),
                            )

                    # ---------------------------------------------
                    # NEW CART
                    # ---------------------------------------------

                    else:

                        RoomPriceCart.objects.create(

                            room=room,

                            cart_name=(
                                cart_data.cart_name
                            ),

                            room_facilities=(
                                cart_data.room_facilities
                                or {}
                            ),

                            base_price=Decimal(
                                str(
                                    cart_data.base_price
                                )
                            ),

                            discount=Decimal(
                                str(
                                    cart_data.discount
                                )
                            ),

                            gst=Decimal(
                                str(
                                    cart_data.gst
                                )
                            ),

                            is_active=(
                                cart_data.is_active
                            ),
                        )

                # =================================================
                # REFRESH ROOM
                # =================================================

                room = (
                    HotelRoom.objects
                    .prefetch_related(
                        "price_carts"
                    )
                    .get(
                        id=room.id
                    )
                )

        except Exception as error:

            return CreateHotelRoomResponse(
                status=0,
                message=str(error),
            )

        # =====================================================
        # SUCCESS
        # =====================================================

        return CreateHotelRoomResponse(
            status=1,
            message="Hotel room updated successfully",
            room=room_type(room),
        )