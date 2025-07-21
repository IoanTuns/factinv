"""factinv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from ariadne_django.views import GraphQLView
from my_company.resolver import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts'), name='accounts'),
    path('', include('core.urls', namespace='core'), name='core'),
    path('company/', include('my_company.urls', namespace='company'), name='company'),
    path('customer/', include('customers.urls', namespace='customer'), name='customer'),
    path('invoice/', include('invoice.urls', namespace='invoice'), name='invoice'),
    # path('graphql/', GraphQLView.as_view(schema=schema), name='graphql'),
    #TODO User Autentification GraphQL
    path('private_graphql/', login_required(GraphQLView.as_view(schema=schema)) , name='graphql'),
    path('graphql/', GraphQLView.as_view(schema=schema) , name='graphql'),
    # path('graphql/', login_required(GraphQLView.as_view(schema=schema)), name='graphql'),
]

# urlpatterns = [
#     path('utilizatori/', Utilizatori.as_view()),        # lista utilizatori
#     path('utilizatori/<int:pk>', Utilizator.as_view()), # un utilizator specific
#     path('facturi/', Facturi.as_view()),                # lista facturi
#     path('facturi/<int:pk>', Factura.as_view()),        # o factura specific
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)