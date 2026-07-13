from strawberry.fastapi import GraphQLRouter

from moviedb.gql.schema import get_graphql_context, schema

router = GraphQLRouter(schema, context_getter=get_graphql_context)
