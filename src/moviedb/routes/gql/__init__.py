from strawberry.fastapi import GraphQLRouter

from moviedb.routes.gql.context import get_graphql_context
from moviedb.routes.gql.schema import schema

router = GraphQLRouter(schema, context_getter=get_graphql_context)
