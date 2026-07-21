

from django.shortcuts import render 
from django.views import View
from authenticatedecorator import jwt_required

from django.utils.decorators import method_decorator
# Create your views here.
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from myapp.account.models import UserRegisterdb
from myapp.follows.models import Follow
from myapp.models import *




@method_decorator(jwt_required, name="dispatch")
class UserProfileAPI(View):
    def post(self, request):
        try:
            user = request.user
            print("UserProfileAPI called")

            followers_count = Follow.objects.filter(
                following=user,
                status=Follow.Status.ACCEPTED
            ).count()

            following_count = Follow.objects.filter(
                follower=user,
                status=Follow.Status.ACCEPTED
            ).count()

            posts = Post.objects.filter(
                creator=user
            ).prefetch_related("media")

            post_count = posts.count()

            total_likes = sum(
                posts.values_list(
                    "like_count",
                    flat=True
                )
            )

            posts_data = []

            for post in posts.order_by("-id")[:20]:

                media_list = []

                for media in post.media.all():

                    media_list.append({
                        "id": media.id,
                        "media_type": media.media_type,
                        "media_url": media.media_url,
                        "thumbnail_url": media.thumbnail_url
                    })

                posts_data.append({
                    "post_id": post.id,
                    "caption": post.caption,
                    "location": post.location,
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "created_at": post.created_at.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),
                    "media": media_list
                })

            return JsonResponse({
                "status": True,
                "data": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "nick_name": user.nick_name,
                    "mobile_no": user.mobileno,
                    "city": user.city,
                    "profile_img": user.profile_img,
                    "bike_image": user.bike_image,
                    "bike_brand_name": user.bike_brand_name,
                    "bike_model": user.bike_model,
                    "vehicle_no": user.vehichle_no,
                    "is_private": user.is_private,
                    "is_verified": user.is_verified,
                    "followers_count": followers_count,
                    "following_count": following_count,
                    "post_count": post_count,
                    "total_likes": total_likes,
                    "posts": posts_data
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