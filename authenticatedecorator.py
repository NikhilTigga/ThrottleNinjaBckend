from functools import wraps
from django.http import JsonResponse
from authentication import get_authenticated_user
from django.utils import timezone

def jwt_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        user = get_authenticated_user(request)
        
       

        if not user:
            return JsonResponse({
                "status": False,
                "refresh_token":"Use Refresh Token",
                "message": "Unauthorized"
            }, status=401)
            
        # Update user's last activity time
        user.last_seen = timezone.now()
        user.save(update_fields=["last_seen"])

        request.user = user

        return view_func(request, *args, **kwargs)

    return wrapper