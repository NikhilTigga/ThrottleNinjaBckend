



import strawberry

@strawberry.type
class UserType:
    id: int
    full_name: str
    nick_name: str
    mobileno: str
    city: str
    profile_img: str | None
    followers_count: int
    following_count: int
    is_verified: bool
    is_private: bool