from django.shortcuts import render 
from django.views import View
from authenticatedecorator import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password

# Create your views here.
from django.http import JsonResponse
from jwt_utils import generate_jwt_token ,generate_refresh_token

from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from imageKit.imagekit_config import imagekit
from myapp.account.models import UserRegisterdb

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(View):

    def post(self, request):
        mobileno = request.POST.get("mobileno")
        password = request.POST.get("password")
        fcm_token = request.POST.get("fcm_token")

        if not mobileno or not password:
            return JsonResponse({
                "status": False,
                "message": "Mobile number and password are required"
            })

        try:
            user = UserRegisterdb.objects.get(mobileno=mobileno)

        except UserRegisterdb.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "User not found"
            })

        if not check_password(password, user.password):
            return JsonResponse({
                "status": False,
                "message": "Invalid password"
            })

        access_token = generate_jwt_token(user)
        refresh_token = generate_refresh_token(user)

        
        user.fcm_token = fcm_token
        user.save()

        return JsonResponse({
            "status": True,
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id
        })
        
        
        
