
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from myapp.account.models import UserRegisterdb


@method_decorator(csrf_exempt, name='dispatch')
class CheckNicknameAvailabilityAPI(View):

    def post(self, request):
        try:
            nick_name = request.POST.get("nick_name")

            if not nick_name:
                return JsonResponse({
                    "status": 0,
                    "message": "nick_name is required"
                })

            nick_name = nick_name.strip()

            exists = UserRegisterdb.objects.filter(
                nick_name__iexact=nick_name
            ).exists()

            if exists:
                return JsonResponse({
                    "status": 0,
                    "available": False,
                    "message": "Nickname is already taken"
                })

            return JsonResponse({
                "status": 1,
                "available": True,
                "message": "Nickname is available"
            })

        except Exception as e:
            return JsonResponse({
                "status": 0,
                "message": str(e)
            })