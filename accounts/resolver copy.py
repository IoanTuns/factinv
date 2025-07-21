from datetime import datetime
from ariadne import QueryType, make_executable_schema, MutationType
from .models import User
from core.ScalarType import datetime_scalar


type_defs= """
scalar EmailAddress
scalar Datetime

type Query{
    all_users: [User]
}

type User {
    id: ID
    email: String!
    first_name: String
    last_name: String
    crate_date: Datetime!
    last_change: Datetime!
    is_admin: Boolean!
    is_staff: Boolean!
    is_active: Boolean!
    is_owner: Boolean!
    is_accsept: Boolean!
}
type Mutation{
    add_user(input: UserInput): UserResults

}
input UserInput {
    email: String!
    first_name: String
    last_name: String
    crate_date: Datetime!
    last_change: Datetime!
    is_admin: Boolean!
    is_staff: Boolean!
    is_active: Boolean!
    is_owner: Boolean!
    is_accsept: Boolean!
}
  type UserResults {
        id: ID!
        email: String!
        first_name: String
        last_name: String
        crate_date: Datetime
        last_change: Datetime
        is_admin: Boolean
        is_staff: Boolean
        is_active: Boolean
        is_owner: Boolean
        is_accsept: Boolean
        err: String
}

"""

query = QueryType()

@query.field('all_users')
def resolve_users(*_):
    return User.objects.all()

mutation = MutationType()

@mutation.field('add_user')
def resolve_add_user(_,info, input):

    user = User.objects.create(
        email=input['email'], 
        first_name=input['first_name'], 
        last_name=input['last_name'], 
        crate_date=datetime.now(),
        last_change=input['last_change'],
        is_admin=input['is_admin'],
        is_staff=input['is_staff'],
        is_active=input['is_active'],
        is_owner=input['is_owner'],
        is_accsept=input['is_accsept']
        )      
    return {'created': True, 'user': user, 'err': None}

schema = make_executable_schema(type_defs, query, mutation, datetime_scalar)