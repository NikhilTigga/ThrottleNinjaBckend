import strawberry

from .users.queries import Query
from graphqlapis.graphql.userLogin.mutation import Mutation

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)