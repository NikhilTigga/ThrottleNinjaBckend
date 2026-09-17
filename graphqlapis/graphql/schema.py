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
from .hotels.hotelprofiles.query import Query as hotelprofileQuery

from .posts.mutations import Mutation as PostMutation
from .userLogin.mutation import Mutation as LoginMutation
from .hotels.hotelsaccount.mutation import Mutation as HotelMutation
from .hotels.hoteledit.mutation import Mutation as EditHotelMutation
from .hotels.hotelRooms.mutation import Mutation as HotelRoomMutation
from .hotels.hotelRooms.editmutation import Mutation as EditHotelRoomMutation
from .hotels.hotelroomlist.queries import Query as HotelRoomQuery

@strawberry.type
class Query(UserQuery, PostQuery
            ,hotelprofileQuery,
              HotelRoomQuery,):
    pass


@strawberry.type
class Mutation(
    PostMutation,
    LoginMutation,
    HotelMutation,
    EditHotelMutation
    ,HotelRoomMutation,
    EditHotelRoomMutation
    
):
    pass

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)