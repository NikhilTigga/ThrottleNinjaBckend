import strawberry
from datetime import datetime


@strawberry.type
class PostMediaType:
    media_url: str
    media_type: str
    thumbnail_url: str | None

@strawberry.type
class PostType:
    id: int
    caption: str | None
    location: str | None
    like_count: int
    comment_count: int
    status: str
    admin_remark: str | None
    created_at: datetime

    creator_id: int
    creator_name: str
    creator_username: str
    
    media: list[PostMediaType] 