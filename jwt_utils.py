import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_jwt_token(user):

    payload = {
        "user_id": user.id,
        "mno": user.mobileno,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token

def generate_refresh_token(user):

    payload = {
        "user_id": user.id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=2),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def generate_hotel_vendor_jwt_token(vendor):
    payload = {
        "vendor_id": vendor.id,
        "mno": vendor.mobile_no,
        "type": "hotel_vendor_access",
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "iat": datetime.utcnow()
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def generate_hotel_vendor_refresh_token(vendor):
    payload = {
        "vendor_id": vendor.id,
        "type": "hotel_vendor_refresh",
        "exp": datetime.utcnow() + timedelta(days=2),
        "iat": datetime.utcnow()
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )




def decode_jwt_token(token):

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        print("Token Expired")
        return None

    except jwt.InvalidTokenError as e:
        print("Invalid Token:", str(e))
        return None