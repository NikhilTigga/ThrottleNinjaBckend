



from django.views import View
from authenticatedecorator import jwt_required
from django.utils.decorators import method_decorator
from myapp.models import Post ,Like , UserRegisterdb
# Create your views here.
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import F


@method_decorator(jwt_required, name='dispatch')
class ToggleLikeAPI(View):

    def post(self, request):
        
        user = request.user

        userid = user.id
        post_id = request.POST.get("post_id")
        if not post_id:
            return JsonResponse({
                "status": False,
                "message": "post_id is required"
            })

        try:
            post = Post.objects.get(id=post_id)
            user = UserRegisterdb.objects.get(id=userid)

        except Post.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Post not found"
            })

        like = Like.objects.filter(
            user=user,
            post=post
        ).first()

        # Unlike
        if like:

            like.delete()

            Post.objects.filter(
                id=post.id,
                like_count__gt=0
            ).update(
                like_count=F("like_count") - 1
            )

            post.refresh_from_db()

            return JsonResponse({
                "status": True,
                "message": "Post unliked",
                "liked": False,
                "like_count": post.like_count
            })

        # Like
        Like.objects.create(
            user=user,
            post=post
        )
        Post.objects.filter(
            id=post.id
        ).update(
            like_count=F("like_count") + 1
        )
        post.refresh_from_db()

        return JsonResponse({
            "status": True,
            "message": "Post liked",
            "liked": True,
            "like_count": post.like_count
        })