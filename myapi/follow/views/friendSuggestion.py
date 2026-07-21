


from django.views import View
from django.http import JsonResponse
from authenticatedecorator import jwt_required
from django.utils.decorators import method_decorator

from myapp.models import *


@method_decorator(jwt_required, name="dispatch")
class FriendSuggestionsAPI(View):

    def post(self, request):
        try:
            current_user = request.user

            if not current_user:
                return JsonResponse({
                    "status": 0,
                    "message": "User not authenticated"
                })

            # Users already followed by current user
            following_ids = Follow.objects.filter(
                follower=current_user,
                status=Follow.Status.ACCEPTED
            ).values_list("following_id", flat=True)

            suggestions = UserRegisterdb.objects.filter(
                is_active=True
            ).exclude(
                id=current_user.id
            ).exclude(
                id__in=following_ids
            ).order_by("-followers_count")[:20]

            data = []

            for user in suggestions:
                data.append({
                    "user_id": user.id,
                    "full_name": user.full_name,
                    "nick_name": user.nick_name,
                    "profile_img": user.profile_img,
                    "followers_count": user.followers_count,
                    "following_count": user.following_count,
                    "is_verified": user.is_verified,
                    "is_private": user.is_private,
                })

            return JsonResponse({
                "status": 1,
                "message": "Friend suggestions fetched successfully",
                "total_users": len(data),
                "data": data
            })

        except Exception as e:
            return JsonResponse({
                "status": 0,
                "message": str(e)
            })


