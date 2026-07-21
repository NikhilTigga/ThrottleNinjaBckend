from jwt_utils import decode_jwt_token
from myapp.account.models import UserRegisterdb


# def get_authenticated_user(request):

#     auth_header = request.headers.get("Authorization")
#     print("Authorization Header:", auth_header)


#     if not auth_header:
#         print("No Authorization header")
#         return None

#     if not auth_header.startswith("Bearer "):
#         print("Invalid Authorization format")
#         return None

#     token = auth_header.split(" ")[1]

#     payload = decode_jwt_token(token)

#     if not payload:
#         return None
#     try:
#         user = UserRegisterdb.objects.get(
#             id=payload["user_id"]
#         )

#         return user

#     except UserRegisterdb.DoesNotExist:
#         return None

def get_authenticated_user(request):

    auth_header = request.headers.get("Authorization")
    # print("Authorization Header:", auth_header)

    if not auth_header:
        print("No Authorization header")
        return None

    if not auth_header.startswith("Bearer "):
        print("Invalid Authorization format")
        return None

    token = auth_header.split(" ")[1]
    print("Token:", token)

    payload = decode_jwt_token(token)
    print("Payload:", payload)

    if not payload:
        print("Payload is None")
        return None

    try:
        user = UserRegisterdb.objects.get(
            id=payload["user_id"]
        )

        print("User Found:", user.id)
        return user

    except UserRegisterdb.DoesNotExist:
        print("User does not exist")
        return None