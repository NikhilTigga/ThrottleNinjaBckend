from authentication import get_authenticated_user ,get_authenticated_hotel_vendor


class GraphQLContext:

    def __init__(self, request):
        self.request = request

        user = get_authenticated_user(request)

        if user:
            request.user = user
        else:
            request.user = None
            
        
        vendor = get_authenticated_hotel_vendor(request)

        if vendor:
            request.hotel_vendor = vendor
        else:
            request.hotel_vendor = None