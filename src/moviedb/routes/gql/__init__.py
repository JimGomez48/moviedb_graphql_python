from strawberry.fastapi import GraphQLRouter

from moviedb.core.gql.context import get_graphql_context
from moviedb.core.gql.schema import schema

router = GraphQLRouter(schema, context_getter=get_graphql_context)
