from django.shortcuts import render 
from django.views import View
from authenticatedecorator import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from django.db.models import F
# Create your views here.
from django.http import JsonResponse
from myapp.models import Post ,Comment
from django.utils.decorators import method_decorator
@method_decorator(jwt_required, name="dispatch")
class AddCommentAPI(View):

    def post(self, request):

        try:
            user = request.user

            post_id = request.POST.get("post_id")
            comment_text = request.POST.get("comment")

            if not post_id:
                return JsonResponse({
                    "status": False,
                    "message": "post_id is required"
                })

            if not comment_text:
                return JsonResponse({
                    "status": False,
                    "message": "comment is required"
                })

            try:
                post = Post.objects.get(id=post_id)

            except Post.DoesNotExist:
                return JsonResponse({
                    "status": False,
                    "message": "Post not found"
                })

            comment = Comment.objects.create(
                user=user,
                post=post,
                comment=comment_text
            )

            Post.objects.filter(
                id=post.id
            ).update(
                comment_count=F("comment_count") + 1
            )

            return JsonResponse({
                "status": True,
                "message": "Comment added successfully",
                "data": {
                    "comment_id": comment.id,
                    "post_id": post.id,
                    "user_id": user.id,
                    "comment": comment.comment,
                    "created_at": comment.created_at
                }
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)