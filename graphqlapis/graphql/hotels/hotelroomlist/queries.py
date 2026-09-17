import json
import strawberry

from strawberry.types import Info

from hotels.models import Hotel, HotelRoom

from .types import (
    HotelRoomlistType,
    HotelRoomDetailType,
    RoomPriceCartType,
    HotelRoomListResponse,
    HotelRoomDetailResponse,
)


@strawberry.type
class Query:

    # =========================================================
    # HOTEL ROOM LIST
    # =========================================================

    @strawberry.field
    def hotel_room_list(
        self,
        info: Info,
    ) -> HotelRoomListResponse:

        # -----------------------------------------------------
        # Authentication
        # -----------------------------------------------------

        vendor = info.context.request.hotel_vendor

        if not vendor:
            return HotelRoomListResponse(
                status=0,
                message="Hotel vendor authentication required",
                rooms=[]
            )

        try:

            # -------------------------------------------------
            # Get logged-in vendor's hotel
            # -------------------------------------------------

            hotel = Hotel.objects.get(
                vendor=vendor
            )

            # -------------------------------------------------
            # Get active rooms of this hotel
            # -------------------------------------------------

            rooms = HotelRoom.objects.filter(
                hotel=hotel,
               
            )

            room_list = []

            for room in rooms:

                room_list.append(
                    HotelRoomlistType(
                        id=room.id,
                        room_name=room.room_name,
                        adults_qty=room.adults_qty,
                        room_images=room.room_images or [],

                        room_features=json.dumps(
                            room.room_features or {}
                        ),

                        amenities=json.dumps(
                            room.amenities or {}
                        ),

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
                    )
                )

            return HotelRoomListResponse(
                status=1,
                message="Room list fetched successfully",
                rooms=room_list
            )

        except Hotel.DoesNotExist:

            return HotelRoomListResponse(
                status=0,
                message="Hotel not found",
                rooms=[]
            )

        except Exception as e:

            return HotelRoomListResponse(
                status=0,
                message=str(e),
                rooms=[]
            )

    # =========================================================
    # HOTEL ROOM DETAILS
    # =========================================================

    @strawberry.field
    def hotel_room_details(
        self,
        info: Info,
        room_id: int,
    ) -> HotelRoomDetailResponse:

        # -----------------------------------------------------
        # Authentication
        # -----------------------------------------------------

        vendor = info.context.request.hotel_vendor

        if not vendor:
            return HotelRoomDetailResponse(
                status=0,
                message="Hotel vendor authentication required",
                room=None
            )

        try:

            # -------------------------------------------------
            # Get logged-in vendor's hotel
            # -------------------------------------------------

            hotel = Hotel.objects.get(
                vendor=vendor
            )

            # -------------------------------------------------
            # Get room ONLY from this vendor's hotel
            # -------------------------------------------------

            room = (
                HotelRoom.objects
                .prefetch_related("price_carts")
                .get(
                    id=room_id,
                    hotel=hotel,
                    
                )
            )

            # -------------------------------------------------
            # Room Price Carts
            # -------------------------------------------------

            carts = []

            for cart in room.price_carts.filter(
                
            ):

                carts.append(
                    RoomPriceCartType(
                        id=cart.id,

                        cart_name=cart.cart_name,

                        room_facilities=json.dumps(
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
                )

            # -------------------------------------------------
            # Room Details
            # -------------------------------------------------

            room_data = HotelRoomDetailType(

                id=room.id,

                room_name=room.room_name,

                adults_qty=room.adults_qty,

                room_images=room.room_images or [],

                room_features=json.dumps(
                    room.room_features or {}
                ),

                amenities=json.dumps(
                    room.amenities or {}
                ),

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

                price_carts=carts,
            )

            return HotelRoomDetailResponse(
                status=1,
                message="Room details fetched successfully",
                room=room_data
            )

        except Hotel.DoesNotExist:

            return HotelRoomDetailResponse(
                status=0,
                message="Hotel not found",
                room=None
            )

        except HotelRoom.DoesNotExist:

            return HotelRoomDetailResponse(
                status=0,
                message="Room not found",
                room=None
            )

        except Exception as e:

            return HotelRoomDetailResponse(
                status=0,
                message=str(e),
                room=None
            )