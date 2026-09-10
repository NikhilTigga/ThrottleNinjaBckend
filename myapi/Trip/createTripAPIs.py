from datetime import timedelta, timezone
import json

from django.db.models import Prefetch
from django.http import JsonResponse
from django.db import transaction
from django.utils.dateparse import parse_date, parse_time
from django.views import View
from django.utils.decorators import method_decorator
from authenticatedecorator import jwt_required

from myapp.models import Trip, TripDay, Club


@method_decorator(jwt_required, name="dispatch")
class CreateTripAPI(View):

    @transaction.atomic
    def post(self, request):

        try:

            user = request.user

            # ==========================================
            # BASIC INFORMATION
            # ==========================================

            trip_name = request.POST.get("trip_name")
            trip_mode = request.POST.get("trip_mode", "group")

            trip_photo = request.FILES.get("trip_photo")

            trip_note = request.POST.get("trip_note")

            # ==========================================
            # DESTINATION
            # ==========================================

            destination_latitude = request.POST.get(
                "destination_latitude"
            )

            destination_longitude = request.POST.get(
                "destination_longitude"
            )

            destination_address = request.POST.get(
                "destination_address"
            )

            # ==========================================
            # MEET-UP POINT
            # ==========================================

            meetup_latitude = request.POST.get(
                "meetup_latitude"
            )

            meetup_longitude = request.POST.get(
                "meetup_longitude"
            )

            meetup_address = request.POST.get(
                "meetup_address"
            )

            meetup_time = request.POST.get(
                "meetup_time"
            )

            # ==========================================
            # CLUB
            # ==========================================

            trip_associated_with_club = request.POST.get(
                "trip_associated_with_club",
                "false"
            )

            club_id = request.POST.get("club_id")

            # Convert string to boolean
            trip_associated_with_club = str(
                trip_associated_with_club
            ).lower() in [
                "true",
                "1",
                "yes"
            ]

            # ==========================================
            # ROUND TRIP
            # ==========================================

            is_round_trip = request.POST.get(
                "is_round_trip",
                "false"
            )

            is_round_trip = str(
                is_round_trip
            ).lower() in [
                "true",
                "1",
                "yes"
            ]

            # ==========================================
            # DURATION
            # ==========================================

            trip_duration_days = request.POST.get(
                "trip_duration_days",
                1
            )

            # ==========================================
            # START DATE
            # ==========================================

            start_date = request.POST.get(
                "start_date"
            )

            # ==========================================
            # PAYMENT TYPE
            # ==========================================

            trip_type = request.POST.get(
                "trip_type",
                "free"
            )

            trip_cost_per_person = request.POST.get(
                "trip_cost_per_person",
                "0"
            )

            # ==========================================
            # VISIBILITY
            # ==========================================

            visibility = request.POST.get(
                "visibility",
                "public"
            )

            # ==========================================
            # POLICIES
            # ==========================================

            cancellation_policy = request.POST.get(
                "cancellation_policy"
            )

            terms_and_conditions = request.POST.get(
                "terms_and_conditions"
            )

            # ==========================================
            # FEATURES
            # ==========================================

            included_feature = request.POST.get(
                "included_feature",
                "[]"
            )

            payment_mode_split_include = request.POST.get(
                "payment_mode_split_include",
                "[]"
            )

            # ==========================================
            # TRIP DAYS
            # ==========================================

            days = request.POST.get(
                "days",
                "[]"
            )

            # ==========================================
            # VALIDATION
            # ==========================================

            if not trip_name:

                return JsonResponse({
                    "status": False,
                    "message": "trip_name is required"
                })

            if trip_mode not in [
                "group",
                "solo"
            ]:

                return JsonResponse({
                    "status": False,
                    "message": "Invalid trip_mode. Use group or solo"
                })

            if trip_type not in [
                "free",
                "split",
                "paid"
            ]:

                return JsonResponse({
                    "status": False,
                    "message": "Invalid trip_type. Use free, split or paid"
                })

            if visibility not in [
                "public",
                "private"
            ]:

                return JsonResponse({
                    "status": False,
                    "message": "Invalid visibility. Use public or private"
                })

            # ==========================================
            # DURATION VALIDATION
            # ==========================================

            try:

                trip_duration_days = int(
                    trip_duration_days
                )

                if trip_duration_days < 1:

                    return JsonResponse({
                        "status": False,
                        "message": "trip_duration_days must be greater than 0"
                    })

            except (ValueError, TypeError):

                return JsonResponse({
                    "status": False,
                    "message": "Invalid trip_duration_days"
                })

            # ==========================================
            # DATE VALIDATION
            # ==========================================

            if not start_date:

                return JsonResponse({
                    "status": False,
                    "message": "start_date is required"
                })

            parsed_start_date = parse_date(
                start_date
            )

            if not parsed_start_date:

                return JsonResponse({
                    "status": False,
                    "message": "Invalid start_date. Use YYYY-MM-DD"
                })

            # ==========================================
            # MEET-UP TIME VALIDATION
            # ==========================================

            parsed_meetup_time = None

            if meetup_time:

                parsed_meetup_time = parse_time(
                    meetup_time
                )

                if not parsed_meetup_time:

                    return JsonResponse({
                        "status": False,
                        "message": "Invalid meetup_time. Use HH:MM:SS"
                    })

            # ==========================================
            # PAYMENT VALIDATION
            # ==========================================

            try:

                trip_cost_per_person = float(
                    trip_cost_per_person
                )

                if trip_cost_per_person < 0:

                    return JsonResponse({
                        "status": False,
                        "message": "trip_cost_per_person cannot be negative"
                    })

            except (ValueError, TypeError):

                return JsonResponse({
                    "status": False,
                    "message": "Invalid trip_cost_per_person"
                })

            # Free trip = cost 0
            if trip_type == "free":

                trip_cost_per_person = 0

            # Paid / Split trip should have cost
            if trip_type in [
                "paid",
                "split"
            ] and trip_cost_per_person <= 0:

                return JsonResponse({
                    "status": False,
                    "message": (
                        "trip_cost_per_person must be greater than 0 "
                        "for paid or split trip"
                    )
                })

            # ==========================================
            # CLUB VALIDATION
            # ==========================================

            club = None

            if trip_associated_with_club:

                if not club_id:

                    return JsonResponse({
                        "status": False,
                        "message": (
                            "club_id is required when "
                            "trip_associated_with_club is true"
                        )
                    })

                try:

                    club = Club.objects.get(
                        id=club_id
                    )

                except Club.DoesNotExist:

                    return JsonResponse({
                        "status": False,
                        "message": "Club not found"
                    })

                # Optional but recommended:
                # only club creator can create
                # a trip associated with the club

                if club.created_by_id != user.id:

                    return JsonResponse({
                        "status": False,
                        "message": (
                            "You are not authorized to "
                            "create a trip for this club"
                        )
                    })

            # ==========================================
            # FEATURES JSON
            # ==========================================

            try:

                included_feature = json.loads(
                    included_feature
                )

                if not isinstance(
                    included_feature,
                    list
                ):

                    return JsonResponse({
                        "status": False,
                        "message": "included_feature must be a JSON array"
                    })

            except json.JSONDecodeError:

                return JsonResponse({
                    "status": False,
                    "message": "Invalid included_feature JSON"
                })

            # ==========================================

            try:

                payment_mode_split_include = json.loads(
                    payment_mode_split_include
                )

                if not isinstance(
                    payment_mode_split_include,
                    list
                ):

                    return JsonResponse({
                        "status": False,
                        "message": (
                            "payment_mode_split_include "
                            "must be a JSON array"
                        )
                    })

            except json.JSONDecodeError:

                return JsonResponse({
                    "status": False,
                    "message": (
                        "Invalid payment_mode_split_include JSON"
                    )
                })

            # ==========================================
            # DAYS JSON
            # ==========================================

            try:

                days = json.loads(days)

                if not isinstance(
                    days,
                    list
                ):

                    return JsonResponse({
                        "status": False,
                        "message": "days must be a JSON array"
                    })

            except json.JSONDecodeError:

                return JsonResponse({
                    "status": False,
                    "message": "Invalid days JSON"
                })

            # ==========================================
            # CHECK NUMBER OF DAYS
            # ==========================================

            if len(days) != trip_duration_days:

                return JsonResponse({
                    "status": False,
                    "message": (
                        f"trip_duration_days is "
                        f"{trip_duration_days}, but "
                        f"{len(days)} day records were provided"
                    )
                })

            # ==========================================
            # CREATE TRIP
            # ==========================================

            trip = Trip.objects.create(

                trip_mode=trip_mode,

                trip_name=trip_name,

                trip_photo=trip_photo,

                trip_note=trip_note,

                # Destination
                destination_latitude=destination_latitude,
                destination_longitude=destination_longitude,
                destination_address=destination_address,

                # Meetup
                meetup_latitude=meetup_latitude,
                meetup_longitude=meetup_longitude,
                meetup_address=meetup_address,
                meetup_time=parsed_meetup_time,

                # Club
                trip_associated_with_club=(
                    trip_associated_with_club
                ),
                club=club,

                # Round trip
                is_round_trip=is_round_trip,

                # Duration
                trip_duration_days=trip_duration_days,

                # Date
                start_date=parsed_start_date,

                # Payment
                trip_type=trip_type,
                trip_cost_per_person=trip_cost_per_person,

                # Visibility
                visibility=visibility,

                # Creator
                created_by=user,

                # Policies
                cancellation_policy=(
                    cancellation_policy
                ),

                terms_and_conditions=(
                    terms_and_conditions
                ),

                # Features
                included_feature=(
                    included_feature
                ),

                payment_mode_split_include=(
                    payment_mode_split_include
                )
            )

            # ==========================================
            # CREATE TRIP DAYS
            # ==========================================

            created_days = []

            for index, day in enumerate(
                days,
                start=1
            ):

                day_number = day.get(
                    "day_number",
                    index
                )

                # ======================================
                # START LOCATION
                # ======================================

                start_location = day.get(
                    "start_location",
                    {}
                )

                # ======================================
                # STOP LOCATION
                # ======================================

                stop_location = day.get(
                    "stop_location",
                    {}
                )

                # ======================================
                # END LOCATION
                # ======================================

                end_location = day.get(
                    "end_location",
                    {}
                )

                # ======================================
                # FLAG OFF TIME
                # ======================================

                flag_off_time = day.get(
                    "flag_off_time"
                )

                parsed_flag_off_time = None

                if flag_off_time:

                    parsed_flag_off_time = parse_time(
                        flag_off_time
                    )

                    if not parsed_flag_off_time:

                        raise ValueError(
                            f"Invalid flag_off_time "
                            f"for day {day_number}"
                        )

                # ======================================
                # CREATE DAY
                # ======================================

                trip_day = TripDay.objects.create(

                    trip=trip,

                    day_number=day_number,

                    # Start location
                    start_location_latitude=(
                        start_location.get(
                            "latitude"
                        )
                    ),

                    start_location_longitude=(
                        start_location.get(
                            "longitude"
                        )
                    ),

                    start_location_address=(
                        start_location.get(
                            "address"
                        )
                    ),

                    # Stop location
                    stop_location_latitude=(
                        stop_location.get(
                            "latitude"
                        )
                    ),

                    stop_location_longitude=(
                        stop_location.get(
                            "longitude"
                        )
                    ),

                    stop_location_address=(
                        stop_location.get(
                            "address"
                        )
                    ),

                    # End location
                    end_location_latitude=(
                        end_location.get(
                            "latitude"
                        )
                    ),

                    end_location_longitude=(
                        end_location.get(
                            "longitude"
                        )
                    ),

                    end_location_address=(
                        end_location.get(
                            "address"
                        )
                    ),

                    # Flag off
                    flag_off_time=(
                        parsed_flag_off_time
                    )
                )

                created_days.append({
                    "id": trip_day.id,
                    "day_number": trip_day.day_number,
                    "start_location": {
                        "latitude": (
                            trip_day.start_location_latitude
                        ),
                        "longitude": (
                            trip_day.start_location_longitude
                        ),
                        "address": (
                            trip_day.start_location_address
                        )
                    },
                    "stop_location": {
                        "latitude": (
                            trip_day.stop_location_latitude
                        ),
                        "longitude": (
                            trip_day.stop_location_longitude
                        ),
                        "address": (
                            trip_day.stop_location_address
                        )
                    },
                    "end_location": {
                        "latitude": (
                            trip_day.end_location_latitude
                        ),
                        "longitude": (
                            trip_day.end_location_longitude
                        ),
                        "address": (
                            trip_day.end_location_address
                        )
                    },
                    "flag_off_time": (
                        str(trip_day.flag_off_time)
                        if trip_day.flag_off_time
                        else None
                    )
                })

            # ==========================================
            # TRIP PHOTO URL
            # ==========================================

            trip_photo_url = None

            if trip.trip_photo:

                trip_photo_url = request.build_absolute_uri(
                    trip.trip_photo.url
                )

            # ==========================================
            # RESPONSE
            # ==========================================

            return JsonResponse({

                "status": True,

                "message": "Trip created successfully",

                "data": {

                    "trip_id": trip.id,

                    "trip_name": trip.trip_name,

                    "trip_mode": trip.trip_mode,

                    "trip_photo": trip_photo_url,

                    "trip_note": trip.trip_note,

                    "destination": {
                        "latitude": (
                            trip.destination_latitude
                        ),
                        "longitude": (
                            trip.destination_longitude
                        ),
                        "address": (
                            trip.destination_address
                        )
                    },

                    "meetup": {
                        "latitude": (
                            trip.meetup_latitude
                        ),
                        "longitude": (
                            trip.meetup_longitude
                        ),
                        "address": (
                            trip.meetup_address
                        ),
                        "time": (
                            str(trip.meetup_time)
                            if trip.meetup_time
                            else None
                        )
                    },

                    "trip_associated_with_club": (
                        trip.trip_associated_with_club
                    ),

                    "club_id": (
                        trip.club_id
                        if trip.club
                        else None
                    ),

                    "is_round_trip": (
                        trip.is_round_trip
                    ),

                    "trip_duration_days": (
                        trip.trip_duration_days
                    ),

                    "start_date": (
                        str(trip.start_date)
                    ),

                    "trip_type": trip.trip_type,

                    "trip_cost_per_person": (
                        str(
                            trip.trip_cost_per_person
                        )
                    ),

                    "visibility": (
                        trip.visibility
                    ),

                    "included_feature": (
                        trip.included_feature
                    ),

                    "payment_mode_split_include": (
                        trip.payment_mode_split_include
                    ),

                    "cancellation_policy": (
                        trip.cancellation_policy
                    ),

                    "terms_and_conditions": (
                        trip.terms_and_conditions
                    ),

                    "created_by": user.id,

                    "days": created_days,

                    "created_at": (
                        trip.created_at
                    )
                }

            }, status=201)

        except ValueError as e:

            return JsonResponse({

                "status": False,

                "message": str(e)

            }, status=400)

        except Exception as e:

            return JsonResponse({

                "status": False,

                "message": str(e)

            }, status=500)
            
            

@method_decorator(jwt_required, name="dispatch")
class UserCreatedTripListAPI(View):

    def post(self, request):

        try:

            user = request.user

            # ==========================================
            # FILTER
            # ==========================================

            trip_filter = request.POST.get(
                "filter",
                "all"
            ).lower()

            if trip_filter not in [
                "all",
                "upcoming",
                "completed"
            ]:

                return JsonResponse({
                    "status": False,
                    "message": (
                        "Invalid filter. "
                        "Use all, upcoming or completed"
                    )
                }, status=400)

            # ==========================================
            # CURRENT DATE
            # ==========================================

            today = timezone.localdate()

            # ==========================================
            # USER CREATED TRIPS
            # ==========================================

            trips = Trip.objects.filter(
                created_by=user
            ).select_related(
                "club"
            ).prefetch_related(
                Prefetch(
                    "days",
                    queryset=TripDay.objects.order_by(
                        "day_number"
                    )
                )
            )

            # ==========================================
            # APPLY FILTER
            # ==========================================

            if trip_filter == "upcoming":

                trips = trips.filter(
                    start_date__gte=today
                )

            elif trip_filter == "completed":

                trips = trips.filter(
                    start_date__lt=today
                )

            # ==========================================
            # ORDER
            # ==========================================

            if trip_filter == "completed":

                trips = trips.order_by(
                    "-start_date"
                )

            else:

                trips = trips.order_by(
                    "start_date"
                )

            # ==========================================
            # RESPONSE DATA
            # ==========================================

            trip_data = []

            for trip in trips:

                # ======================================
                # TRIP PHOTO
                # ======================================

                trip_photo_url = None

                if trip.trip_photo:

                    trip_photo_url = (
                        request.build_absolute_uri(
                            trip.trip_photo.url
                        )
                    )

                # ======================================
                # TRIP STATUS
                # ======================================

                if trip.start_date >= today:

                    trip_status = "upcoming"

                else:

                    trip_status = "completed"

                # ======================================
                # CLUB
                # ======================================

                club_data = None

                if trip.club:

                    club_data = {
                        "club_id": trip.club.id,
                        "club_name": trip.club.name
                    }

                # ======================================
                # DAYS
                # ======================================

                days_data = []

                for day in trip.days.all():

                    days_data.append({

                        "id": day.id,

                        "day_number": (
                            day.day_number
                        ),

                        "start_location": {

                            "latitude": (
                                day.start_location_latitude
                            ),

                            "longitude": (
                                day.start_location_longitude
                            ),

                            "address": (
                                day.start_location_address
                            )
                        },

                        "stop_location": {

                            "latitude": (
                                day.stop_location_latitude
                            ),

                            "longitude": (
                                day.stop_location_longitude
                            ),

                            "address": (
                                day.stop_location_address
                            )
                        },

                        "end_location": {

                            "latitude": (
                                day.end_location_latitude
                            ),

                            "longitude": (
                                day.end_location_longitude
                            ),

                            "address": (
                                day.end_location_address
                            )
                        },

                        "flag_off_time": (

                            str(day.flag_off_time)

                            if day.flag_off_time

                            else None
                        )
                    })

                # ======================================
                # TRIP DATA
                # ======================================

                trip_data.append({

                    "trip_id": trip.id,

                    "trip_name": trip.trip_name,

                    "trip_mode": trip.trip_mode,

                    "trip_status": trip_status,

                    "trip_photo": trip_photo_url,

                    "trip_note": trip.trip_note,

                    # ----------------------------------
                    # DESTINATION
                    # ----------------------------------

                    "destination": {

                        "latitude": (
                            trip.destination_latitude
                        ),

                        "longitude": (
                            trip.destination_longitude
                        ),

                        "address": (
                            trip.destination_address
                        )
                    },

                    # ----------------------------------
                    # MEETUP
                    # ----------------------------------

                    "meetup": {

                        "latitude": (
                            trip.meetup_latitude
                        ),

                        "longitude": (
                            trip.meetup_longitude
                        ),

                        "address": (
                            trip.meetup_address
                        ),

                        "time": (

                            str(trip.meetup_time)

                            if trip.meetup_time

                            else None
                        )
                    },

                    # ----------------------------------
                    # CLUB
                    # ----------------------------------

                    "trip_associated_with_club": (
                        trip.trip_associated_with_club
                    ),

                    "club": club_data,

                    # ----------------------------------
                    # TRIP DETAILS
                    # ----------------------------------

                    "is_round_trip": (
                        trip.is_round_trip
                    ),

                    "trip_duration_days": (
                        trip.trip_duration_days
                    ),

                    "start_date": (
                        str(trip.start_date)
                    ),

                    # ----------------------------------
                    # PAYMENT
                    # ----------------------------------

                    "trip_type": (
                        trip.trip_type
                    ),

                    "trip_cost_per_person": (
                        str(
                            trip.trip_cost_per_person
                        )
                    ),

                    # ----------------------------------
                    # VISIBILITY
                    # ----------------------------------

                    "visibility": (
                        trip.visibility
                    ),

                    # ----------------------------------
                    # FEATURES
                    # ----------------------------------

                    "included_feature": (
                        trip.included_feature
                    ),

                    "payment_mode_split_include": (
                        trip.payment_mode_split_include
                    ),

                    # ----------------------------------
                    # POLICIES
                    # ----------------------------------

                    "cancellation_policy": (
                        trip.cancellation_policy
                    ),

                    "terms_and_conditions": (
                        trip.terms_and_conditions
                    ),

                    # ----------------------------------
                    # CREATOR
                    # ----------------------------------

                    "created_by": (
                        trip.created_by_id
                    ),

                    # ----------------------------------
                    # DAYS
                    # ----------------------------------

                    "days": days_data,

                    # ----------------------------------
                    # CREATED DATE
                    # ----------------------------------

                    "created_at": (
                        trip.created_at
                    ),

                    "updated_at": (
                        trip.updated_at
                    )
                })

            # ==========================================
            # RESPONSE
            # ==========================================

            return JsonResponse({

                "status": True,

                "message": (
                    "Created trips fetched successfully"
                ),

                "filter": trip_filter,

                "total_trips": len(trip_data),

                "data": trip_data

            }, status=200)

        except Exception as e:

            return JsonResponse({

                "status": False,

                "message": str(e)

            }, status=500)
            
@method_decorator(jwt_required, name="dispatch")
class DiscoverTripAPI(View):

    def post(self, request):

        try:

            user = request.user

            # ==========================================
            # FILTER
            # ==========================================

            trip_filter = request.POST.get(
                "filter",
                "all"
            ).lower().strip()

            valid_filters = [
                "all",
                "nearby",
                "one_day",
                "multi_day"
            ]

            if trip_filter not in valid_filters:

                return JsonResponse({
                    "status": False,
                    "message": (
                        "Invalid filter. Use all, nearby, "
                        "one_day or multi_day"
                    )
                }, status=400)

            # ==========================================
            # TODAY
            # ==========================================

            today = timezone.localdate()

            # ==========================================
            # BASE QUERY
            # ==========================================
            # Only PUBLIC trips
            #
            # Trip is not expired if:
            #
            # start_date + duration - 1 >= today
            #
            # Example:
            # start_date = 2026-09-08
            # duration = 3
            #
            # End date = 2026-09-10
            # ==========================================

            trips = (
                Trip.objects
                .filter(
                    visibility="public"
                )
                .select_related(
                    "created_by",
                    "club"
                )
                .prefetch_related(
                    Prefetch(
                        "days",
                        queryset=TripDay.objects.order_by(
                            "day_number"
                        )
                    )
                )
                .order_by("start_date")
            )

            # ==========================================
            # REMOVE EXPIRED TRIPS
            # ==========================================

            valid_trips = []

            for trip in trips:

                trip_end_date = (
                    trip.start_date
                    + timedelta(
                        days=trip.trip_duration_days - 1
                    )
                )

                if trip_end_date >= today:

                    valid_trips.append(
                        trip
                    )

            # ==========================================
            # FILTER: ONE DAY
            # ==========================================

            if trip_filter == "one_day":

                valid_trips = [
                    trip
                    for trip in valid_trips
                    if trip.trip_duration_days == 1
                ]

            # ==========================================
            # FILTER: MULTI DAY
            # ==========================================

            elif trip_filter == "multi_day":

                valid_trips = [
                    trip
                    for trip in valid_trips
                    if trip.trip_duration_days > 1
                ]

            # ==========================================
            # FILTER: NEARBY
            # ==========================================

            elif trip_filter == "nearby":

                user_lat = user.current_lat
                user_long = user.current_long

                if user_lat is None or user_long is None:

                    return JsonResponse({
                        "status": False,
                        "message": (
                            "Your current location is not available. "
                            "Please update your current latitude "
                            "and longitude first."
                        )
                    }, status=400)

                user_lat = float(user_lat)
                user_long = float(user_long)

                nearby_trips = []

                for trip in valid_trips:

                    if (
                        trip.destination_latitude is None
                        or trip.destination_longitude is None
                    ):
                        continue

                    trip_lat = float(
                        trip.destination_latitude
                    )

                    trip_long = float(
                        trip.destination_longitude
                    )

                    # ======================================
                    # HAVERSINE DISTANCE
                    # ======================================

                    from math import radians, sin, cos, sqrt, atan2

                    R = 6371  # Earth radius in KM

                    lat1 = radians(user_lat)
                    lat2 = radians(trip_lat)

                    delta_lat = radians(
                        trip_lat - user_lat
                    )

                    delta_long = radians(
                        trip_long - user_long
                    )

                    a = (
                        sin(delta_lat / 2) ** 2
                        + cos(lat1)
                        * cos(lat2)
                        * sin(delta_long / 2) ** 2
                    )

                    c = 2 * atan2(
                        sqrt(a),
                        sqrt(1 - a)
                    )

                    distance_km = R * c

                    # ======================================
                    # NEARBY = WITHIN 50 KM
                    # ======================================

                    if distance_km <= 50:

                        nearby_trips.append(
                            (
                                trip,
                                round(
                                    distance_km,
                                    2
                                )
                            )
                        )

                # nearest trip first

                nearby_trips.sort(
                    key=lambda x: x[1]
                )

                # ==========================================
                # RESPONSE DATA FOR NEARBY
                # ==========================================

                trip_data = []

                for trip, distance_km in nearby_trips:

                    trip_data.append(
                        self.build_trip_data(
                            request,
                            trip,
                            today,
                            distance_km
                        )
                    )

                return JsonResponse({

                    "status": True,

                    "message": (
                        "Nearby trips fetched successfully"
                    ),

                    "filter": trip_filter,

                    "nearby_radius_km": 50,

                    "total_trips": len(
                        trip_data
                    ),

                    "data": trip_data

                }, status=200)

            # ==========================================
            # NORMAL FILTER RESPONSE
            # ==========================================

            trip_data = []

            for trip in valid_trips:

                trip_data.append(
                    self.build_trip_data(
                        request,
                        trip,
                        today
                    )
                )

            return JsonResponse({

                "status": True,

                "message": (
                    "Discover trips fetched successfully"
                ),

                "filter": trip_filter,

                "total_trips": len(
                    trip_data
                ),

                "data": trip_data

            }, status=200)

        # ==============================================
        # ERRORS
        # ==============================================

        except Exception as e:

            return JsonResponse({

                "status": False,

                "message": str(e)

            }, status=500)

    # ==================================================
    # BUILD TRIP RESPONSE
    # ==================================================

    def build_trip_data(
        self,
        request,
        trip,
        today,
        distance_km=None
    ):

        # ==========================================
        # TRIP PHOTO
        # ==========================================

        trip_photo_url = None

        if trip.trip_photo:

            trip_photo_url = request.build_absolute_uri(
                trip.trip_photo.url
            )

        # ==========================================
        # END DATE
        # ==========================================

        trip_end_date = (
            trip.start_date
            + timedelta(
                days=trip.trip_duration_days - 1
            )
        )

        # ==========================================
        # TRIP STATUS
        # ==========================================

        if trip.start_date > today:

            trip_status = "upcoming"

        elif (
            trip.start_date <= today
            <= trip_end_date
        ):

            trip_status = "ongoing"

        else:

            trip_status = "completed"

        # ==========================================
        # CLUB
        # ==========================================

        club_data = None

        if trip.club:

            club_data = {

                "club_id": trip.club.id,

                "club_name": trip.club.name,

                "club_image": (
                    request.build_absolute_uri(
                        trip.club.club_image.url
                    )
                    if trip.club.club_image
                    else None
                )

            }

        # ==========================================
        # CREATED BY
        # ==========================================

        creator = trip.created_by

        creator_data = {

            "user_id": creator.id,

            "full_name": creator.full_name,

            "nick_name": creator.nick_name,

            "profile_img": creator.profile_img,

            "bike_brand_name": (
                creator.bike_brand_name
            ),

            "bike_model": (
                creator.bike_model
            )

        }

        # ==========================================
        # TRIP DAYS
        # ==========================================

        days_data = []

        for day in trip.days.all():

            days_data.append({

                "id": day.id,

                "day_number": (
                    day.day_number
                ),

                "start_location": {

                    "latitude": (
                        day.start_location_latitude
                    ),

                    "longitude": (
                        day.start_location_longitude
                    ),

                    "address": (
                        day.start_location_address
                    )

                },

                "stop_location": {

                    "latitude": (
                        day.stop_location_latitude
                    ),

                    "longitude": (
                        day.stop_location_longitude
                    ),

                    "address": (
                        day.stop_location_address
                    )

                },

                "end_location": {

                    "latitude": (
                        day.end_location_latitude
                    ),

                    "longitude": (
                        day.end_location_longitude
                    ),

                    "address": (
                        day.end_location_address
                    )

                },

                "flag_off_time": (

                    str(day.flag_off_time)

                    if day.flag_off_time

                    else None

                )

            })

        # ==========================================
        # FINAL DATA
        # ==========================================

        data = {

            "trip_id": trip.id,

            "trip_name": trip.trip_name,

            "trip_mode": trip.trip_mode,

            "trip_status": trip_status,

            "trip_photo": trip_photo_url,

            "trip_note": trip.trip_note,

            # --------------------------------------
            # DESTINATION
            # --------------------------------------

            "destination": {

                "latitude": (
                    trip.destination_latitude
                ),

                "longitude": (
                    trip.destination_longitude
                ),

                "address": (
                    trip.destination_address
                )

            },

            # --------------------------------------
            # MEETUP
            # --------------------------------------

            "meetup": {

                "latitude": (
                    trip.meetup_latitude
                ),

                "longitude": (
                    trip.meetup_longitude
                ),

                "address": (
                    trip.meetup_address
                ),

                "time": (

                    str(trip.meetup_time)

                    if trip.meetup_time

                    else None

                )

            },

            # --------------------------------------
            # CLUB
            # --------------------------------------

            "trip_associated_with_club": (
                trip.trip_associated_with_club
            ),

            "club": club_data,

            # --------------------------------------
            # TRIP SETTINGS
            # --------------------------------------

            "is_round_trip": (
                trip.is_round_trip
            ),

            "trip_duration_days": (
                trip.trip_duration_days
            ),

            "start_date": (
                str(trip.start_date)
            ),

            "end_date": (
                str(trip_end_date)
            ),

            # --------------------------------------
            # PAYMENT
            # --------------------------------------

            "trip_type": (
                trip.trip_type
            ),

            "trip_cost_per_person": (
                str(
                    trip.trip_cost_per_person
                )
            ),

            # --------------------------------------
            # VISIBILITY
            # --------------------------------------

            "visibility": (
                trip.visibility
            ),

            # --------------------------------------
            # FEATURES
            # --------------------------------------

            "included_feature": (
                trip.included_feature
            ),

            "payment_mode_split_include": (
                trip.payment_mode_split_include
            ),

            # --------------------------------------
            # POLICIES
            # --------------------------------------

            "cancellation_policy": (
                trip.cancellation_policy
            ),

            "terms_and_conditions": (
                trip.terms_and_conditions
            ),

            # --------------------------------------
            # CREATOR
            # --------------------------------------

            "created_by": creator_data,

            # --------------------------------------
            # DAYS
            # --------------------------------------

            "days": days_data,

            # --------------------------------------
            # DISTANCE
            # --------------------------------------

            "distance_km": (
                distance_km
            )

        }

        return data