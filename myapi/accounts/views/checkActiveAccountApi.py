

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

# class CheckActiveAccountApi(View):
#     def post(self, request):
        
#         user_id = request.POST.get("user_id")
        
#         if not user_id:
#             return JsonResponse({
#                 "status":False,
#                 "message":"user_id is required"
#             })
        
#         try:
#             user = UserRegisterdb.objects.filter(id = user_id).first()
            
#             if user:
#                 return JsonResponse({
#                     "status":True,
#                     "User_Active":True
#                 })
#             else:
#                 return JsonResponse({
                    
#                 })
                
            