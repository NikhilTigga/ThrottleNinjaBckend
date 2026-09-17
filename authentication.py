from jwt_utils import decode_jwt_token
from myapp.account.models import UserRegisterdb

from hotels.models import HotelVendor


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
    

    payload = decode_jwt_token(token)
   

    if not payload:
        print("Payload is None")
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    try:
        user = UserRegisterdb.objects.get(
            id=user_id
        )

        print("User Found:", user.id)
        return user

    except UserRegisterdb.DoesNotExist:
        print("User does not exist")
        return None
    



def get_authenticated_hotel_vendor(request):
    
    auth_header = request.headers.get("Authorization")
    # print("Authorization Header:", auth_header)

    if not auth_header:
        print("No Authorization header")
        return None

    if not auth_header.startswith("Bearer "):
        print("Invalid Authorization format")
        return None

    token = auth_header.split(" ")[1]
    

    payload = decode_jwt_token(token)
    

    if not payload:
        print("Payload is None")
        return None

    vendor_id = payload.get("vendor_id")
    if not vendor_id:
        return None

    try:
        user = HotelVendor.objects.get(
            id=vendor_id
        )

        print("User Found:", user.id)
        return user

    except HotelVendor.DoesNotExist:
        print("User does not exist")
        return None

