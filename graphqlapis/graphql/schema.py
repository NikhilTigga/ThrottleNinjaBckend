# import strawberry

# from .users.queries import Query as UserQuery
# from .posts.queries import Query as PostQuery

# from .posts.mutations import Mutation as PostMutation

# @strawberry.type
# class Query(UserQuery, PostQuery):
#     pass

# schema = strawberry.Schema(query=Query)




# @strawberry.type
# class Mutation(PostMutation):
#     pass

# schema = strawberry.Schema(query=Query, mutation=Mutation)


import strawberry

from .users.queries import Query as UserQuery
from .posts.queries import Query as PostQuery

from .posts.mutations import Mutation as PostMutation
from .userLogin.mutation import Mutation as LoginMutation


@strawberry.type
class Query(UserQuery, PostQuery):
    pass


@strawberry.type
class Mutation(
    PostMutation,
    LoginMutation
):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)