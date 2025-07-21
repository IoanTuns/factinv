from datetime import datetime
from email.mime import application
# from accounts import graphql_config
from ariadne import QueryType, load_schema_from_path, make_executable_schema, MutationType
from .models import User
from core.ScalarType import datetime_scalar
from ariadne import MutationType
from django.contrib import auth 
from ariadne.wsgi import GraphQL

# query = QueryType("UserAuthMutation")

# @query.field("LoginPayload")
# def resolve_login(_, info, email, password):
#     request = info.context["request"]
#     user = auth.authenticate(email, password)
#     if user:
#         auth.login(request, email)
#         return {"status": True, "email": email}
#     return {"status": False, "error": "Invalid username or password"}

# def resolve_logout(_, info):
#     request = info.context["request"]
#     if request.user.is_authenticated:
#         auth.logout(request)
#         return True
#     return False

# @query.field('all_users')
# def resolve_users(*_):
#     return User.objects.all()

# mutation = MutationType()

# @mutation.field('add_user')
# def resolve_add_user(_,info, input):

#     user = User.objects.create(
#         email=input['email'], 
#         first_name=input['first_name'], 
#         last_name=input['last_name'], 
#         crate_date=datetime.now(),
#         last_change=input['last_change'],
#         is_admin=input['is_admin'],
#         is_staff=input['is_staff'],
#         is_active=input['is_active'],
#         is_owner=input['is_owner'],
#         is_accsept=input['is_accsept']
#         )      
#     return {'created': True, 'user': user, 'err': None}

# schema = make_executable_schema(schema, query)
# application = GraphQL(schema)