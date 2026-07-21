

from django.shortcuts import render 
from django.views import View
from authenticatedecorator import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password

# Create your views here.
from django.http import JsonResponse
from jwt_utils import generate_jwt_token

from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from imageKit.imagekit_config import imagekit
from myapp.account.models import UserRegisterdb



@method_decorator(csrf_exempt, name='dispatch')   
class UserRegisterAPI(View):
    def post(self, request):
        full_name = request.POST.get("full_name")
        password = request.POST.get("password")
        nick_name = request.POST.get("nick_name")
        mobile_no = request.POST.get("mobile_no")
        city = request.POST.get("city")
        profile_img = request.FILES.get("profile_image")
        
        print("Profile Image is ",profile_img)
        if not full_name or not nick_name or not mobile_no or not city or not password:
            return JsonResponse({
                "status":False,
                "message":"All fields are required",
            }, status = 200)
            
        if UserRegisterdb.objects.filter(mobileno = mobile_no).exists():
            return JsonResponse({
                "status":False,
                "message":"User already Exist"
            }, status= 200)
            
        if UserRegisterdb.objects.filter(nick_name = nick_name).exclude():
            return JsonResponse({
                "status":False,
                "message":"User nick name Already Exists",
            }, status = 200)
            
        hashed_password = make_password(password)
        
        profile_url = None
        profile_file_id = None

        if profile_img:
            upload = imagekit.files.upload(
                file=profile_img.read(),
                file_name=profile_img.name,
                use_unique_file_name=True,
                folder="/profile_images"
            )

            profile_url = upload.url
            profile_file_id = upload.file_id
            
        createuser = UserRegisterdb.objects.create(
            full_name=full_name,
            nick_name=nick_name,
            mobileno=mobile_no,
            city=city,
            password=hashed_password,
            profile_img=profile_url,
            profile_img_fileid=profile_file_id,
        )
        return JsonResponse({
            "status": True,
            "message": "User registered successfully",
            "user_id": createuser.id
        }, status=201)