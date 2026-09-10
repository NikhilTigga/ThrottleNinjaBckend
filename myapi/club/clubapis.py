from math import atan2, cos, radians, sin, sqrt

from django.db.models import Q, Count
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from myapp.models import Club ,ClubMember, ClubJoinRequest
from authenticatedecorator import jwt_required

@method_decorator(jwt_required, name="dispatch")
class CreateClubAPI(View):
    def post(self, request):
        try:
            user = request.user

            name = request.POST.get("name")
            description = request.POST.get("description", "")
            club_address = request.POST.get("club_address", "")
            club_latitude = request.POST.get("club_latitude")
            club_longitude = request.POST.get("club_longitude")
            visibility = request.POST.get("visibility", "public")

            club_image = request.FILES.get("club_image")

            if not name:
                return JsonResponse({
                    "status": False,
                    "message": "Club name is required"
                })

            club = Club.objects.create(
                name=name,
                description=description,
                club_address=club_address,
                club_latitude=club_latitude if club_latitude else None,
                club_longitude=club_longitude if club_longitude else None,
                created_by=user,
                visibility=visibility
            )

            if club_image:
                club.club_image = club_image
                club.save()

            return JsonResponse({
                "status": True,
                "message": "Club created successfully",
                "data": {
                    "club_id": club.id,
                    "name": club.name,
                    "description": club.description,
                    "club_address": club.club_address,
                    "club_latitude": str(club.club_latitude) if club.club_latitude else None,
                    "club_longitude": str(club.club_longitude) if club.club_longitude else None,
                    "visibility": club.visibility,
                    "club_image": club.club_image.url if club.club_image else None,
                    "created_by": user.id,
                    "created_at": club.created_at
                }
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)
            

@method_decorator(jwt_required, name="dispatch")
class JoinClubAPI(View):

    def post(self, request):

        try:

            user = request.user

            club_id = request.POST.get("club_id")

            if not club_id:
                return JsonResponse({
                    "status": False,
                    "message": "club_id is required"
                })

            # ==========================================
            # GET CLUB
            # ==========================================

            try:

                club = Club.objects.get(
                    id=club_id
                )

            except Club.DoesNotExist:

                return JsonResponse({
                    "status": False,
                    "message": "Club not found"
                })

            # ==========================================
            # CHECK ALREADY MEMBER
            # ==========================================

            already_member = ClubMember.objects.filter(
                club=club,
                user=user
            ).exists()

            if already_member:

                return JsonResponse({
                    "status": False,
                    "message": "You are already a member of this club"
                })

            # ==========================================
            # PUBLIC CLUB
            # ==========================================

            if club.visibility == "public":

                ClubMember.objects.create(
                    club=club,
                    user=user
                )

                return JsonResponse({
                    "status": True,
                    "message": "Joined club successfully",
                    "data": {
                        "club_id": club.id,
                        "user_id": user.id,
                        "status": "joined"
                    }
                })

            # ==========================================
            # PRIVATE CLUB
            # ==========================================

            join_request, created = ClubJoinRequest.objects.get_or_create(
                club=club,
                user=user,
                defaults={
                    "status": "pending"
                }
            )

            if not created:

                if join_request.status == "pending":

                    return JsonResponse({
                        "status": False,
                        "message": "Join request already sent"
                    })

                elif join_request.status == "approved":

                    return JsonResponse({
                        "status": False,
                        "message": "Your request is already approved"
                    })

                elif join_request.status == "rejected":

                    join_request.status = "pending"
                    join_request.save()

            return JsonResponse({
                "status": True,
                "message": "Join request sent successfully",
                "data": {
                    "club_id": club.id,
                    "user_id": user.id,
                    "status": "pending"
                }
            })

        except Exception as e:

            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)
            

@method_decorator(jwt_required, name="dispatch")
class ApproveClubJoinRequestAPI(View):

    def post(self, request):

        try:

            user = request.user

            request_id = request.POST.get("request_id")

            if not request_id:

                return JsonResponse({
                    "status": False,
                    "message": "request_id is required"
                })

            # ==========================================
            # GET REQUEST
            # ==========================================

            try:

                join_request = ClubJoinRequest.objects.select_related(
                    "club",
                    "user"
                ).get(
                    id=request_id
                )

            except ClubJoinRequest.DoesNotExist:

                return JsonResponse({
                    "status": False,
                    "message": "Join request not found"
                })

            club = join_request.club

            # ==========================================
            # CHECK ADMIN
            # ==========================================

            if club.created_by_id != user.id:

                return JsonResponse({
                    "status": False,
                    "message": "You are not authorized to approve this request"
                })

            # ==========================================
            # CHECK STATUS
            # ==========================================

            if join_request.status != "pending":

                return JsonResponse({
                    "status": False,
                    "message": f"Request is already {join_request.status}"
                })

            # ==========================================
            # CREATE MEMBER
            # ==========================================

            ClubMember.objects.get_or_create(
                club=club,
                user=join_request.user
            )

            # ==========================================
            # UPDATE REQUEST
            # ==========================================

            join_request.status = "approved"
            join_request.save()

            return JsonResponse({
                "status": True,
                "message": "Join request approved successfully",
                "data": {
                    "request_id": join_request.id,
                    "club_id": club.id,
                    "user_id": join_request.user.id,
                    "status": "approved"
                }
            })

        except Exception as e:

            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)
            

@method_decorator(jwt_required, name="dispatch")
class RejectClubJoinRequestAPI(View):

    def post(self, request):

        try:

            user = request.user

            request_id = request.POST.get("request_id")

            if not request_id:

                return JsonResponse({
                    "status": False,
                    "message": "request_id is required"
                })

            try:

                join_request = ClubJoinRequest.objects.select_related(
                    "club",
                    "user"
                ).get(
                    id=request_id
                )

            except ClubJoinRequest.DoesNotExist:

                return JsonResponse({
                    "status": False,
                    "message": "Join request not found"
                })

            club = join_request.club

            # ==========================================
            # CHECK ADMIN
            # ==========================================

            if club.created_by_id != user.id:

                return JsonResponse({
                    "status": False,
                    "message": "You are not authorized to reject this request"
                })

            if join_request.status != "pending":

                return JsonResponse({
                    "status": False,
                    "message": f"Request is already {join_request.status}"
                })

            join_request.status = "rejected"
            join_request.save()

            return JsonResponse({
                "status": True,
                "message": "Join request rejected successfully",
                "data": {
                    "request_id": join_request.id,
                    "club_id": club.id,
                    "user_id": join_request.user.id,
                    "status": "rejected"
                }
            })

        except Exception as e:

            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)
            
            


@method_decorator(jwt_required, name="dispatch")
class UserClubListAPI(View):

    def post(self, request):

        try:

            user = request.user

            # ==========================================
            # FILTER
            # ==========================================

            club_filter = request.POST.get(
                "filter",
                "active"
            ).lower().strip()

            if club_filter not in [
                "all",
                "active",
                "deactivated"
            ]:
                return JsonResponse({
                    "status": False,
                    "message": (
                        "Invalid filter. Use all, active "
                        "or deactivated"
                    )
                }, status=400)

            # ==========================================
            # USER CLUBS
            # ==========================================
            # User can be:
            # 1. Club owner
            # 2. Club member
            # ==========================================

            clubs = (
                Club.objects
                .filter(
                    Q(created_by=user) |
                    Q(members__user=user)
                )
                .select_related(
                    "created_by"
                )
                .distinct()
            )

            # ==========================================
            # ACTIVE FILTER
            # ==========================================

            if club_filter == "active":

                clubs = clubs.filter(
                    is_active=True
                )

            # ==========================================
            # DEACTIVATED FILTER
            # ==========================================

            elif club_filter == "deactivated":

                clubs = clubs.filter(
                    is_active=False
                )

            # ==========================================
            # ORDER
            # ==========================================

            clubs = clubs.order_by(
                "-created_at"
            )

            # ==========================================
            # RESPONSE
            # ==========================================

            club_data = []

            for club in clubs:

                # ======================================
                # CLUB IMAGE
                # ======================================

                club_image_url = None

                if club.club_image:

                    club_image_url = request.build_absolute_uri(
                        club.club_image.url
                    )

                # ======================================
                # CLUB IMG
                # ======================================

                club_img_url = None

                if club.club_img:

                    club_img_url = request.build_absolute_uri(
                        club.club_img.url
                    )

                # ======================================
                # CHECK USER ROLE
                # ======================================

                if club.created_by_id == user.id:

                    user_role = "owner"

                else:

                    user_role = "member"

                # ======================================
                # MEMBER COUNT
                # ======================================

                member_count = ClubMember.objects.filter(
                    club=club
                ).count()

                # ======================================
                # CLUB DATA
                # ======================================

                club_data.append({

                    "club_id": club.id,

                    "name": club.name,

                    "description": club.description,

                    "club_address": club.club_address,

                    "club_latitude": (
                        str(club.club_latitude)
                        if club.club_latitude
                        else None
                    ),

                    "club_longitude": (
                        str(club.club_longitude)
                        if club.club_longitude
                        else None
                    ),

                    "club_image": club_image_url,

                    "club_img": club_img_url,

                    "visibility": club.visibility,

                    "is_active": club.is_active,

                    "user_role": user_role,

                    "member_count": member_count,

                    "created_by": club.created_by_id,

                    "created_at": club.created_at

                })

            # ==========================================
            # FINAL RESPONSE
            # ==========================================

            return JsonResponse({

                "status": True,

                "message": (
                    "User clubs fetched successfully"
                ),

                "filter": club_filter,

                "total_clubs": len(club_data),

                "data": club_data

            }, status=200)

        except Exception as e:

            return JsonResponse({

                "status": False,

                "message": str(e)

            }, status=500)
            
            
@method_decorator(jwt_required, name="dispatch")
class DiscoverClubAPI(View):

    def post(self, request):

        try:

            user = request.user

            # ==========================================
            # FILTER
            # ==========================================

            club_filter = request.POST.get(
                "filter",
                "all"
            ).lower().strip()

            valid_filters = [
                "all",
                "around_you",
                "most_active"
            ]

            if club_filter not in valid_filters:

                return JsonResponse({
                    "status": False,
                    "message": (
                        "Invalid filter. Use all, "
                        "around_you or most_active"
                    )
                }, status=400)

            # ==========================================
            # BASE QUERY
            # ==========================================
            # Only:
            # - Active clubs
            # - Public clubs
            # - Clubs where current user is NOT already
            #   owner/member
            # ==========================================

            clubs = (
                Club.objects
                .filter(
                    is_active=True,
                    visibility="public"
                )
                .exclude(
                    Q(created_by=user) |
                    Q(members__user=user)
                )
                .annotate(
                    member_count=Count(
                        "members",
                        distinct=True
                    )
                )
                .select_related(
                    "created_by"
                )
                .distinct()
            )

            # ==========================================
            # AROUND YOU
            # ==========================================

            if club_filter == "around_you":

                user_lat = user.current_lat
                user_long = user.current_long

                if (
                    user_lat is None
                    or user_long is None
                ):

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

                nearby_clubs = []

                for club in clubs:

                    if (
                        club.club_latitude is None
                        or club.club_longitude is None
                    ):
                        continue

                    club_lat = float(
                        club.club_latitude
                    )

                    club_long = float(
                        club.club_longitude
                    )

                    # ==================================
                    # HAVERSINE DISTANCE
                    # ==================================

                    R = 6371  # Earth radius in KM

                    lat1 = radians(user_lat)
                    lat2 = radians(club_lat)

                    delta_lat = radians(
                        club_lat - user_lat
                    )

                    delta_long = radians(
                        club_long - user_long
                    )

                    a = (
                        sin(delta_lat / 2) ** 2
                        +
                        cos(lat1)
                        * cos(lat2)
                        * sin(delta_long / 2) ** 2
                    )

                    c = 2 * atan2(
                        sqrt(a),
                        sqrt(1 - a)
                    )

                    distance_km = R * c

                    # ==================================
                    # WITHIN 50 KM
                    # ==================================

                    if distance_km <= 50:

                        nearby_clubs.append(
                            (
                                club,
                                round(
                                    distance_km,
                                    2
                                )
                            )
                        )

                # Nearest club first

                nearby_clubs.sort(
                    key=lambda x: x[1]
                )

                club_data = []

                for club, distance_km in nearby_clubs:

                    club_data.append(
                        self.build_club_data(
                            request,
                            club,
                            distance_km
                        )
                    )

                return JsonResponse({

                    "status": True,

                    "message": (
                        "Nearby clubs fetched successfully"
                    ),

                    "filter": club_filter,

                    "nearby_radius_km": 50,

                    "total_clubs": len(
                        club_data
                    ),

                    "data": club_data

                }, status=200)

            # ==========================================
            # MOST ACTIVE
            # ==========================================

            if club_filter == "most_active":

                clubs = clubs.order_by(
                    "-member_count",
                    "-created_at"
                )

            # ==========================================
            # ALL
            # ==========================================

            else:

                clubs = clubs.order_by(
                    "-created_at"
                )

            # ==========================================
            # BUILD RESPONSE
            # ==========================================

            club_data = []

            for club in clubs:

                club_data.append(
                    self.build_club_data(
                        request,
                        club
                    )
                )

            # ==========================================
            # RESPONSE
            # ==========================================

            return JsonResponse({

                "status": True,

                "message": (
                    "Discover clubs fetched successfully"
                ),

                "filter": club_filter,

                "total_clubs": len(
                    club_data
                ),

                "data": club_data

            }, status=200)

        except Exception as e:

            return JsonResponse({

                "status": False,

                "message": str(e)

            }, status=500)

    # ==================================================
    # BUILD CLUB RESPONSE
    # ==================================================

    def build_club_data(
        self,
        request,
        club,
        distance_km=None
    ):

        # ==========================================
        # CLUB IMAGE
        # ==========================================

        club_image_url = None

        if club.club_image:

            club_image_url = request.build_absolute_uri(
                club.club_image.url
            )

        # ==========================================
        # CLUB IMG
        # ==========================================

        club_img_url = None

        if club.club_img:

            club_img_url = request.build_absolute_uri(
                club.club_img.url
            )

        # ==========================================
        # CREATOR
        # ==========================================

        creator = club.created_by

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
        # MEMBER COUNT
        # ==========================================

        # member_count comes from annotation.
        # Fallback is useful if this method is reused.

        member_count = getattr(
            club,
            "member_count",
            None
        )

        if member_count is None:

            member_count = ClubMember.objects.filter(
                club=club
            ).count()

        # ==========================================
        # RESPONSE
        # ==========================================

        return {

            "club_id": club.id,

            "name": club.name,

            "description": club.description,

            "club_address": club.club_address,

            "club_latitude": (
                str(club.club_latitude)
                if club.club_latitude is not None
                else None
            ),

            "club_longitude": (
                str(club.club_longitude)
                if club.club_longitude is not None
                else None
            ),

            "club_image": club_image_url,

            "club_img": club_img_url,

            "visibility": club.visibility,

            "is_active": club.is_active,

            "member_count": member_count,

            "created_by": creator_data,

            "distance_km": distance_km,

            "created_at": club.created_at

        }