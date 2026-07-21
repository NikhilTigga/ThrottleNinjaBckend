from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from authenticatedecorator import jwt_required
from myapp.models import *

@method_decorator(jwt_required, name="dispatch")
class FollowersListAPI(View):

    def post(self, request):

        try:
            user = request.user

            followers = Follow.objects.filter(
                following=user,
                status=Follow.Status.ACCEPTED
            ).select_related("follower")

            data = []

            for follow in followers:

                follower = follow.follower

                data.append({
                    "user_id": follower.id,
                    "full_name": follower.full_name,
                    "nick_name": follower.nick_name,
                    "profile_img": follower.profile_img,
                    "is_verified": follower.is_verified,
                    "city": follower.city,
                })

            return JsonResponse({
                "status": True,
                "count": len(data),
                "followers": data
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            })