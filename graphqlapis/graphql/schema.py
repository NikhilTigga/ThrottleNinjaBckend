

import strawberry
from .users.queries import Query

schema = strawberry.Schema(query=Query)