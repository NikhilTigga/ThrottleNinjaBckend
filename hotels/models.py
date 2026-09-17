from django.db import models

from .hotels_register.hotelregisterdb import Hotel, HotelReview, HotelRoom, HotelVendor, RoomPriceCart

__all__ = [
	"HotelVendor",
	"Hotel",
	"HotelRoom",
	"RoomPriceCart",
	"HotelReview",
]
