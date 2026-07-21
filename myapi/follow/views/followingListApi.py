
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from myapp.models import *
from authenticatedecorator import jwt_required



@method_decorator(jwt_required, name="dispatch")
class FollowingListAPI(View):

    def post(self, request):

        try:
            user = request.user

            following_users = Follow.objects.filter(
                follower=user,
                status=Follow.Status.ACCEPTED
            ).select_related("following")

            data = []

            for follow in following_users:

                following = follow.following

                data.append({
                    "user_id": following.id,
                    "full_name": following.full_name,
                    "nick_name": following.nick_name,
                    "profile_img": following.profile_img,
                    "is_verified": following.is_verified,
                    "city": following.city,
                })

            return JsonResponse({
                "status": True,
                "count": len(data),
                "following": data
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            })