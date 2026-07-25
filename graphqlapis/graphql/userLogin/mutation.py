from django.contrib.auth.hashers import check_password
import strawberry

from myapp.models import UserRegisterdb
from graphqlapis.graphql.userLogin.types import LoginResponse
from jwt_utils import generate_jwt_token, generate_refresh_token


@strawberry.mutation
def login(self, mobileno: str, password: str) -> LoginResponse:

    try:
        user = UserRegisterdb.objects.get(
            mobileno=mobileno
        )

        if not check_password(password, user.password):
            return LoginResponse(
                status=0,
                message="Invalid password",
                access_token=None,
                refresh_token=None
            )

        access_token = generate_jwt_token(user)
        refresh_token = generate_refresh_token(user)

        return LoginResponse(
            status=1,
            message="Login successful",
            access_token=access_token,
            refresh_token=refresh_token
        )

    except UserRegisterdb.DoesNotExist:
        return LoginResponse(
            status=0,
            message="User not found",
            access_token=None,
            refresh_token=None
        )


@strawberry.type
class Mutation:
    login = login