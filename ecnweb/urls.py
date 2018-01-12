"""ecnweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView

import station.views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^$', station.views.home, name='home'),
    # ex: /station/4
    url(r'^station/(?P<station_id>\d+)/$', station.views.station_detail, name='station_detail'),
]
