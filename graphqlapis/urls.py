from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from graphqlapis.graphql.schema import schema

from .context import GraphQLContext


urlpatterns = [
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                schema=schema,
                get_context=lambda request, response: GraphQLContext(request),
                multipart_uploads_enabled=True,
            )
        ),
    ),
]