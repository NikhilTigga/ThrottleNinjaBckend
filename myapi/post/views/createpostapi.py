from django.shortcuts import render 
from django.views import View
from authenticatedecorator import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password

# Create your views here.
from django.http import JsonResponse
from jwt_utils import generate_jwt_token

from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from imageKit.imagekit_config import imagekit
from myapp.account.models import UserRegisterdb
from myapp.follows.models import Follow
from myapp.feed.models import Userfeed
from myapp.models import Hashtag
from myapp.posts.models import Post , PostMedia



from videoUploadHelper.uploadVideo import upload_feed_video

@method_decorator(jwt_required, name='dispatch')
class CreatePostAPI(View):

    def post(self, request):
        user = request.user
        user_id = user.id
        caption = request.POST.get("caption", "")
        location = request.POST.get("location")
        hashtags = request.POST.get("hashtags", "")

        if not user_id:
            return JsonResponse({
                "status": False,
                "message": "user_id required"
            })

        try:
            user = UserRegisterdb.objects.get(id=user_id)

        except UserRegisterdb.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "User not found"
            })

        files = request.FILES.getlist("media")

        if not files:
            return JsonResponse({
                "status": False,
                "message": "Upload at least one file"
            })

        post = Post.objects.create(
            creator=user,
            caption=caption,
            location = location,
        )
        
        # Add creator's own post to feed
        Userfeed.objects.create(
            user=user,
            post=post,
            creator=user
        )
        
        for tag in hashtags.split(","):
            tag = tag.strip().lstrip("#").lower()

            if tag:
                hashtag_obj, created = Hashtag.objects.get_or_create(
                    name=tag
                )
                post.hashtags.add(hashtag_obj)

        # Get all accepted followers
        followers = Follow.objects.filter(
            following=user,
            status=Follow.Status.ACCEPTED
        ).values_list("follower_id", flat=True)

        # Bulk create feed entries
        feed_entries = [
            Userfeed(
                user_id=follower_id,
                post=post,
                creator=user
            )
            for follower_id in followers
        ]

        Userfeed.objects.bulk_create(
            feed_entries,
            ignore_conflicts=True
        )

        media_response = []

        for media_file in files:

            extension = media_file.name.split(".")[-1].lower()

            video_extensions = [
                "mp4",
                "mov",
                "avi",
                "mkv",
                "webm",
            ]

            if extension in video_extensions:

                result = upload_feed_video(media_file)

                media_obj = PostMedia.objects.create(
                    post=post,
                    media_url=result["video_url"],
                    thumbnail_url=result["thumbnail_url"],
                    media_id=result.get("video_file_id"),
                    media_thumbnail_id=result["thumbnail_file_id"],
                    media_type="video",
                )

            else:

                upload = imagekit.files.upload(
                    file=media_file.read(),
                    file_name=media_file.name,
                    use_unique_file_name=True,
                    folder="/feeds/images",
                )

                media_obj = PostMedia.objects.create(
                    post=post,
                    media_url=upload.url,
                    media_id=upload.file_id,
                    media_type="image",
                )

            media_response.append({
                "id": media_obj.id,
                "type": media_obj.media_type,
                "url": media_obj.media_url,
                "thumbnail": media_obj.thumbnail_url,
            })

        return JsonResponse({
            "status": True,
            "message": "Post uploaded successfully",
            "post_id": post.id,
            "media": media_response,
        })