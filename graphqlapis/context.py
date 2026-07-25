from authentication import get_authenticated_user


class GraphQLContext:

    def __init__(self, request):
        self.request = request

        user = get_authenticated_user(request)

        if user:
            request.user = user
        else:
            request.user = None