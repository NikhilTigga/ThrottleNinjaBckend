
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from authenticatedecorator import jwt_required
from myapp.models import ChatRoom

@method_decorator(jwt_required, name="dispatch")
class ChatUserListAPI(View):

    def post(self, request):

        try:
            user = request.user

            rooms = (
                ChatRoom.objects
                .filter(users=user)
                .prefetch_related("users")
            )

            data = []

            for room in rooms:

                other_users = room.users.exclude(
                    id=user.id
                )

                for other_user in other_users:

                    data.append({
                        "room_id": room.id,
                        "room_key": room.room_key,

                        "user_id": other_user.id,
                        "full_name": other_user.full_name,
                        "nick_name": other_user.nick_name,
                        "profile_img": other_user.profile_img,
                        "is_verified": other_user.is_verified,
                        "city": other_user.city,
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