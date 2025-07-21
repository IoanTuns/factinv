from ariadne import QueryType, make_executable_schema, MutationType
from .models import MyCompany, UsersAndCompany
from factinv.graphql_config import type_defs

query = QueryType()

@query.field('my_companies')
def resolve_companies(*_):    
    return MyCompany.objects.all()


# Selectare compani curente pentru utilizatorul autentificat
# @query.field('my_companies')
# def resolve_companies(*_, info):
#     #Filtrare tabel UsersAndCompany cu utilizatorul autentificat
#     own_company = UsersAndCompany.objects.current_company(user=info.context.user)
#     # Selectare detalii pentru companiile asociate
#     comany_list = MyCompany.objects.owner_company(cui = own_company)
#     print(comany_list)
#     return MyCompany.objects.owner_company(cui = own_company)


schema = make_executable_schema(type_defs, query)