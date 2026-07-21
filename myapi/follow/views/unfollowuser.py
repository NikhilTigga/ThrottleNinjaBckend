from django.views import View
from django.http import JsonResponse
from authenticatedecorator import jwt_required
from django.utils.decorators import method_decorator

from myapp.models import *



@method_decorator(jwt_required, name="dispatch")
class UnfollowUserAPI(View):

    def post(self, request):

        try:
            user = request.user

            following_id = request.POST.get("following_id")

            deleted_count, _ = Follow.objects.filter(
                follower=user,
                following_id=following_id
            ).delete()

            if deleted_count == 0:
                return JsonResponse({
                    "status": False,
                    "message": "Follow relation not found"
                })

            return JsonResponse({
                "status": True,
                "message": "User unfollowed successfully"
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            })