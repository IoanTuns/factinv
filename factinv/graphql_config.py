from ariadne import QueryType, make_executable_schema, load_schema_from_path, MutationType
from ariadne import MutationType

type_defs = [
    # load_schema_from_path("ariadne_tutorial/schema.graphql"),
    load_schema_from_path("./factinv/schema.graphql"),
]

# query_user = QueryType()
# # query_user.set_field("all_users", resolver.resolve_users)

# mutation = MutationType()
# mutation.set_field("login", resolver.resolve_login)
# mutation.set_field("logout", resolver.resolve_logout)

# schema = make_executable_schema(type_defs, query_user, mutation)