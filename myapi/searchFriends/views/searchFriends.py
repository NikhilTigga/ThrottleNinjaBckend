from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator

from authenticatedecorator import jwt_required
from myapp.models import UserRegisterdb, Follow

@method_decorator(jwt_required, name="dispatch")
class SearchFriendsAPI(View):
    def post(self, request):
        try:
            user = request.user

            keyword = request.POST.get(
                "keyword",
                ""
            ).strip()

            if not keyword:
                return JsonResponse({
                    "status": False,
                    "message": "keyword is required"
                })

            users = UserRegisterdb.objects.filter(
                nick_name__icontains=keyword,
                is_active=True
            ).exclude(
                id=user.id
            )[:20]

            following_ids = set(
                Follow.objects.filter(
                    follower=user,
                    status=Follow.Status.ACCEPTED
                ).values_list(
                    "following_id",
                    flat=True
                )
            )

            data = []
            for item in users:
                data.append({
                    "user_id": item.id,
                    "full_name": item.full_name,
                    "nick_name": item.nick_name,
                    "profile_img": item.profile_img,
                    "city": item.city,
                    "is_verified": item.is_verified,
                    "followers_count": item.followers_count,
                    "following_count": item.following_count,
                    "is_private": item.is_private,
                    "is_following": item.id in following_ids
                })

            return JsonResponse({
                "status": True,
                "count": len(data),
                "users": data
            })

        except Exception as e:

            return JsonResponse({
                "status": False,
                "message": str(e)
            })