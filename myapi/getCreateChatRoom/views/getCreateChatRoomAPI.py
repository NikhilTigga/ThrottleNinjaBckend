from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from authenticatedecorator import jwt_required

from myapp.models import (
    UserRegisterdb,
    ChatRoom,
    Follow
)

@method_decorator(jwt_required, name="dispatch")
class getCreateChatRoomAPI(View):

    def post(self, request):

        try:

            current_user = request.user

            other_user_id = request.POST.get(
                "other_user_id"
            )

            if not other_user_id:
                return JsonResponse({
                    "status": False,
                    "message": "other_user_id required"
                })

            other_user = UserRegisterdb.objects.get(
                id=other_user_id
            )

            is_following = Follow.objects.filter(
                follower=current_user,
                following=other_user,
                status=Follow.Status.ACCEPTED
            ).exists()

            if not is_following:
                return JsonResponse({
                    "status": False,
                    "message": "Follow user first"
                })

            user_ids = sorted([
                current_user.id,
                other_user.id
            ])

            room_key = f"{user_ids[0]}_{user_ids[1]}"

            room, created = ChatRoom.objects.get_or_create(
                room_key=room_key
            )

            # Add users only when room is newly created
            if created:
                room.users.add(
                    current_user,
                    other_user
                )

            return JsonResponse({
                "status": True,
                "room_id": room.id,
                "room_key": room.room_key,
                "is_new": created
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