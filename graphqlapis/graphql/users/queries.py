

import strawberry
from myapp.models import UserRegisterdb
from .types  import UserType


@strawberry.type
class Query:

    @strawberry.field
    def users(self) -> list[UserType]:

        users = UserRegisterdb.objects.filter(
            is_active=True
        )

        return [
            UserType(
                id=user.id,
                full_name=user.full_name,
                nick_name=user.nick_name,
                mobileno=user.mobileno,
                city=user.city,
                profile_img=user.profile_img,
                followers_count=user.followers_count,
                following_count=user.following_count,
                is_verified=user.is_verified,
                is_private=user.is_private,
            )
            for user in users
        ]