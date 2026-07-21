


from django.views import View
from authenticatedecorator import jwt_required

from django.utils.decorators import method_decorator

from myapp.models import Userfeed ,Like , Follow

# Create your views here.
from django.http import JsonResponse

from random import shuffle
from django.utils.decorators import method_decorator
from myapi.helperfunction import get_user_status

# @method_decorator(jwt_required, name="dispatch")
# class GetFeedAPI(View):

#     def post(self, request):

#         try:
#             user = request.user

#             # Following users feed
#             following_feeds = list(
#                 Userfeed.objects.filter(
#                     user=user
#                 ).select_related(
#                     "post",
#                     "creator"
#                 ).prefetch_related(
#                     "post__media"
#                 ).order_by("-id")[:20]
#             )

#             feed_post_ids = [
#                 item.post_id
#                 for item in following_feeds
#             ]

#             # Explore posts
#             random_posts = list(
#                 Userfeed.objects.exclude(
#                     creator=user
#                 ).exclude(
#                     post_id__in=feed_post_ids
#                 ).select_related(
#                     "post",
#                     "creator"
#                 ).prefetch_related(
#                     "post__media"
#                 ).order_by("?")[:5]
#             )

#             response_data = []

#             # Following feed posts
#             for item in following_feeds:

#                 media_data = []

#                 for media in item.post.media.all():
#                     media_data.append({
#                         "type": media.media_type,
#                         "url": media.media_url,
#                         "thumbnail": media.thumbnail_url,
#                     })

#                 response_data.append({
#                     "post_id": item.post.id,
#                     "caption": item.post.caption,
#                     "creator_id": item.creator.id,
#                     "creator_name": item.creator.full_name,
#                     "like_count": item.post.like_count,
#                     "comment_count": item.post.comment_count,
#                     "is_explore": False,
#                     "created_at": item.post.created_at,
#                     "media": media_data,
#                 })

#             # Explore posts
#             for item in random_posts:

#                 media_data = []

#                 for media in item.post.media.all():
#                     media_data.append({
#                         "type": media.media_type,
#                         "url": media.media_url,
#                         "thumbnail": media.thumbnail_url,
#                     })

#                 response_data.append({
#                     "post_id": item.post.id,
#                     "caption": item.post.caption,
#                     "creator_id": item.creator.id,
#                     "creator_name": item.creator.full_name,
#                     "like_count": item.post.like_count,
#                     "comment_count": item.post.comment_count,
#                     "is_explore": True,
#                     "created_at": item.post.created_at,
#                     "media": media_data,
#                 })

#             shuffle(response_data)

#             return JsonResponse({
#                 "status": True,
#                 "count": len(response_data),
#                 "data": response_data,
#             })

#         except Exception as e:
#             import traceback
#             traceback.print_exc()

#             return JsonResponse({
#                 "status": False,
#                 "message": str(e)
#             }, status=500)
        
        
        
# @method_decorator(jwt_required, name="dispatch")
# class GetFeedAPI(View):

#     def post(self, request):

#         try:
#             user = request.user

#             # Get all liked post ids by current user
#             liked_post_ids = set(
#                 Like.objects.filter(
#                     user=user
#                 ).values_list(
#                     "post_id",
#                     flat=True
#                 )
#             )

#             # Following users feed
#             following_feeds = list(
#                 Userfeed.objects.filter(
#                     user=user
#                 ).select_related(
#                     "post",
#                     "creator"
#                 ).prefetch_related(
#                     "post__media",
#                     "post__comments__user"
#                 ).order_by("-id")[:20]
#             )

#             feed_post_ids = [
#                 item.post_id
#                 for item in following_feeds
#             ]

#             # Explore posts
#             random_posts = list(
#                 Userfeed.objects.exclude(
#                     creator=user
#                 ).exclude(
#                     post_id__in=feed_post_ids
#                 ).select_related(
#                     "post",
#                     "creator"
#                 ).prefetch_related(
#                     "post__media",
#                     "post__comments__user"
#                 ).order_by("?")[:5]
#             )

#             response_data = []

#             all_feeds = following_feeds + random_posts

#             for item in all_feeds:

#                 # Media
#                 media_data = []
#                 for media in item.post.media.all():
#                     media_data.append({
#                         "type": media.media_type,
#                         "url": media.media_url,
#                         "thumbnail": media.thumbnail_url,
#                     })

#                 # Comments
#                 comments_data = []
#                 for comment in item.post.comments.all():
#                     comments_data.append({
#                         "comment_id": comment.id,
#                         "user_id": comment.user.id,
#                         "user_name": comment.user.full_name,
#                         "comment": comment.comment,
#                         "created_at": comment.created_at,
#                     })
#                 following_user_ids = set(
#                     Follow.objects.filter(
#                         follower=user,
#                         status=Follow.Status.ACCEPTED
#                     ).values_list(
#                         "following_id",
#                         flat=True
#                     )
#                 )
                
#                 liked_post_ids = set(
#                     Like.objects.filter(
#                         user=user
#                     ).values_list(
#                         "post_id",
#                         flat=True
#                     )
#                 )

#                 response_data.append({
#                     "post_id": item.post.id,
#                     "caption": item.post.caption,

#                     "creator_id": item.creator.id,
#                     "creator_name": item.creator.full_name,

#                     "like_count": item.post.like_count,
#                     "comment_count": item.post.comment_count,

#                     # New Fields
#                     "is_my_post": item.creator_id == user.id,
#                     "is_liked": item.post.id in liked_post_ids,
#                     "is_explore": item in random_posts,
                    
                    
#                     "is_following": item.creator_id in following_user_ids,

#                     "created_at": item.post.created_at,

#                     "media": media_data,
#                     "comments": comments_data,
#                 })

#             shuffle(response_data)

#             return JsonResponse({
#                 "status": True,
#                 "count": len(response_data),
#                 "data": response_data,
#             })

#         except Exception as e:
#             import traceback
#             traceback.print_exc()

#             return JsonResponse({
#                 "status": False,
#                 "message": str(e)
#             }, status=500)



@method_decorator(jwt_required, name="dispatch")
class GetFeedAPI(View):

    def post(self, request):

        try:
            user = request.user

            # Posts liked by current user
            liked_post_ids = set(
                Like.objects.filter(
                    user=user
                ).values_list(
                    "post_id",
                    flat=True
                )
            )

            # Users followed by current user
            following_user_ids = set(
                Follow.objects.filter(
                    follower=user,
                    status=Follow.Status.ACCEPTED
                ).values_list(
                    "following_id",
                    flat=True
                )
            )

            # Following feed
            following_feeds = list(
                Userfeed.objects.filter(
                    user=user
                ).select_related(
                    "post",
                    "creator"
                ).prefetch_related(
                    "post__media",
                    "post__comments__user"
                ).order_by("-id")[:20]
            )

            feed_post_ids = [
                item.post_id
                for item in following_feeds
            ]

            # Explore feed
            random_posts = list(
                Userfeed.objects.exclude(
                    creator=user
                ).exclude(
                    post_id__in=feed_post_ids
                ).select_related(
                    "post",
                    "creator"
                ).prefetch_related(
                    "post__media",
                    "post__comments__user"
                ).order_by("?")[:5]
            )

            all_feeds = following_feeds + random_posts

            response_data = []

            for item in all_feeds:

                # Media Data
                # Separate Images and Videos
                images = []
                videos = []

                for media in item.post.media.all():

                    media_info = {
                        "id": media.id,
                        "url": media.media_url,
                        "thumbnail": media.thumbnail_url,
                    }

                    if media.media_type == "image":
                        images.append(media_info)

                    elif media.media_type == "video":
                        videos.append(media_info)

                # Comments Data
                comments_data = []

                for comment in item.post.comments.all():
                    comments_data.append({
                        "comment_id": comment.id,
                        "user_id": comment.user.id,
                        "user_name": comment.user.full_name,
                        "comment": comment.comment,
                        "created_at": comment.created_at,
                    })
                creator_status = get_user_status(item.creator)
                

                response_data.append({
                    "post_id": item.post.id,
                    "caption": item.post.caption,
                    

                    "creator_id": item.creator.id,
                    "creator_name": item.creator.full_name,
                    "is_online": creator_status["is_online"],
                    "status_text": creator_status["status_text"],
                    
                    "profile_img":item.creator.profile_img,

                    "like_count": item.post.like_count,
                    "comment_count": item.post.comment_count,

                    # Flags
                    "is_my_post": item.creator_id == user.id,
                    "is_liked": item.post.id in liked_post_ids,
                    "is_explore": item in random_posts,
                    "is_following": (
                        False
                        if item.creator_id == user.id
                        else item.creator_id in following_user_ids
                    ),

                    "created_at": item.post.created_at,

                    "images": images,
                    "videos": videos,
                    "comments": comments_data,
                })

            shuffle(response_data)

            return JsonResponse({
                "status": True,
                "count": len(response_data),
                "data": response_data,
            })

        except Exception as e:
            import traceback
            traceback.print_exc()

            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)