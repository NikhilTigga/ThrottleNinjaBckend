

from django.shortcuts import render 
from django.views import View
from authenticatedecorator import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from myapp.account.models import UserRegisterdb
# Create your views here.
from django.http import JsonResponse
from jwt_utils import generate_jwt_token

from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from imageKit.imagekit_config import imagekit

# @method_decorator(jwt_required, name="dispatch")
# class UpdateProfileAPI(View):

#     def post(self, request):

#         user_id = request.user

#         if not user_id:
#             return JsonResponse({
#                 "status": False,
#                 "message": "user_id is required"
#             })

#         try:
#             user = UserRegisterdb.objects.get(id=user_id)
#         except UserRegisterdb.DoesNotExist:
#             return JsonResponse({
#                 "status": False,
#                 "message": "User not found"
#             })

#         # Text fields
#         full_name = request.POST.get("full_name")
#         city = request.POST.get("city")
#         password = request.POST.get("password")
#         bike_brand_name = request.POST.get("bike_brand_name")
#         bike_model = request.POST.get("bike_model")
#         manufacturing_year = request.POST.get("manufacturing_year")
#         vehichle_no = request.POST.get("vehichle_no")

#         # Image fields
#         profile_img = request.FILES.get("profile_img")
#         bike_image = request.FILES.get("bike_image")

#         if full_name:
#             user.full_name = full_name

#         if city:
#             user.city = city

#         if password:
#             user.password = password

#         if bike_brand_name:
#             user.bike_brand_name = bike_brand_name

#         if bike_model:
#             user.bike_model = bike_model

#         if manufacturing_year:
#             user.manufacturing_year = manufacturing_year

#         if vehichle_no:
#             user.vehichle_no = vehichle_no

#         if profile_img:
#             user.profile_img = profile_img

#         if bike_image:
#             user.bike_image = bike_image

#         try:
#             user.save()

#             return JsonResponse({
#                 "status": True,
#                 "message": "Profile updated successfully"
#             })

#         except Exception as e:
#             return JsonResponse({
#                 "status": False,
#                 "message": str(e)
#             })


@method_decorator(jwt_required, name="dispatch")
class UpdateProfileAPI(View):

    def post(self, request):
        try:
            user = request.user

            if not user:
                return JsonResponse({
                    "status": False,
                    "message": "User not authenticated"
                })

            full_name = request.POST.get("full_name")
            city = request.POST.get("city")
            password = request.POST.get("password")
            bike_brand_name = request.POST.get("bike_brand_name")
            bike_model = request.POST.get("bike_model")
            manufacturing_year = request.POST.get("manufacturing_year")
            vehichle_no = request.POST.get("vehichle_no")

            if full_name:
                user.full_name = full_name

            if city:
                user.city = city

            if password:
                user.password = password

            if bike_brand_name:
                user.bike_brand_name = bike_brand_name

            if bike_model:
                user.bike_model = bike_model

            if manufacturing_year:
                user.manufacturing_year = manufacturing_year

            if vehichle_no:
                user.vehichle_no = vehichle_no

            user.save()

            return JsonResponse({
                "status": True,
                "message": "Profile updated successfully"
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            })