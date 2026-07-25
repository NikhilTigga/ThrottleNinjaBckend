import strawberry
from django.utils import timezone

from myapp.models import Post


@strawberry.type
class Mutation:

    @strawberry.mutation
    def block_post(
        self,
        post_id: int,
        remark: str
    ) -> str:

        try:
            post = Post.objects.get(id=post_id)

            post.status = "blocked"
            post.admin_remark = remark
            post.moderated_at = timezone.now()
            post.save()

            return "Post blocked successfully"

        except Post.DoesNotExist:
            return "Post not found"
        
        

@strawberry.mutation
def unblock_post(
    self,
    post_id: int
) -> str:

    try:
        post = Post.objects.get(id=post_id)

        post.status = "active"
        post.admin_remark = ""
        post.save()

        return "Post unblocked successfully"

    except Post.DoesNotExist:
        return "Post not found"