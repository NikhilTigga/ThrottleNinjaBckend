import strawberry
from typing import Optional


@strawberry.type
class LoginResponse:
    status: int
    message: str
    access_token: Optional[str]
    refresh_token: Optional[str]