import strawberry

from myapp.models import Post 
from .types import PostType , PostMediaType
from strawberry.types import Info

@strawberry.type
class Query:

    @strawberry.field
    def admin_posts(self, info: Info) -> list[PostType]:
        user = info.context.request.user

        if not user:
            raise Exception("Unauthorized")

        posts = (
            Post.objects
            .select_related("creator")
            .order_by("-created_at")
        )

        return [
            PostType(
                id=post.id,
                caption=post.caption,
                location=post.location,
                like_count=post.like_count,
                comment_count=post.comment_count,
                status=post.status,
                admin_remark=post.admin_remark,
                created_at=post.created_at,

                creator_id=post.creator.id,
                creator_name=post.creator.full_name,
                creator_username=post.creator.nick_name,

                media=[
                    PostMediaType(
                        media_url=media.media_url,
                        media_type=media.media_type,
                        thumbnail_url=media.thumbnail_url,
                    )
                    for media in post.media.all()
                ]
            )
            for post in posts
        ]