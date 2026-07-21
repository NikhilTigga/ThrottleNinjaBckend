

from django.shortcuts import render 
from django.views import View
from authenticatedecorator import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password

# Create your views here.
from django.http import JsonResponse
from jwt_utils import generate_jwt_token ,generate_refresh_token ,decode_jwt_token

from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from imageKit.imagekit_config import imagekit
from myapp.account.models import UserRegisterdb

@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenAPI(View):

    def post(self, request):

        refresh_token = request.POST.get("refresh_token")

        if not refresh_token:
            return JsonResponse({
                "status": False,
                "message": "Refresh token is required"
            })

        payload = decode_jwt_token(refresh_token)

        if not payload:
            return JsonResponse({
                "status": False,
                "message": "Invalid or expired refresh token"
            })

        if payload.get("type") != "refresh":
            return JsonResponse({
                "status": False,
                "message": "Invalid token type"
            })

        try:
            user = UserRegisterdb.objects.get(
                id=payload["user_id"]
            )
        except UserRegisterdb.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "User not found"
            })

        access_token = generate_jwt_token(user)
        refresh_token = generate_refresh_token(user)

        return JsonResponse({
            "status": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
        })