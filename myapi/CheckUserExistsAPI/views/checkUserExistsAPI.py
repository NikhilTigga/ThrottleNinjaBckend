from django.http import JsonResponse
from myapp.models import UserRegisterdb
from django.views import View


class CheckUserExistsAPI(View):

    def post(self, request):

        try:
            user_id = request.POST.get("user_id")

            if not user_id:
                return JsonResponse({
                    "status": False,
                    "message": "user_id is required"
                })

            try:
                user = UserRegisterdb.objects.get(id=user_id)

                return JsonResponse({
                    "status": True,
                    "message": "User found",
                    "user": {
                        "id": user.id,
                        "full_name": user.full_name,
                        "nick_name": user.nick_name,
                        "mobileno": user.mobileno,
                        "profile_img": user.profile_img,
                        "city": user.city,
                        "is_verified": user.is_verified,
                        "is_private": user.is_private,
                        "is_active": user.is_active,
                        "followers_count": user.followers_count,
                        "following_count": user.following_count,
                    }
                })

            except UserRegisterdb.DoesNotExist:
                return JsonResponse({
                    "status": False,
                    "message": "User not found"
                })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            })