from django.views import View
from django.http import JsonResponse
from authenticatedecorator import jwt_required
from django.utils.decorators import method_decorator

from myapp.models import *
@method_decorator(jwt_required, name="dispatch")


class FollowUserAPI(View):

    def post(self, request):

        try:
            user = request.user

            following_id = request.POST.get("following_id")

            if not following_id:
                return JsonResponse({
                    "status": False,
                    "message": "following_id is required"
                })

            if str(user.id) == str(following_id):
                return JsonResponse({
                    "status": False,
                    "message": "You cannot follow yourself"
                })

            try:
                following_user = UserRegisterdb.objects.get(
                    id=following_id
                )
            except UserRegisterdb.DoesNotExist:
                return JsonResponse({
                    "status": False,
                    "message": "User not found"
                })

            follow_obj, created = Follow.objects.get_or_create(
                follower=user,
                following=following_user
            )

            if not created:
                return JsonResponse({
                    "status": False,
                    "message": "Already following this user"
                })

            return JsonResponse({
                "status": True,
                "message": "User followed successfully"
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            })