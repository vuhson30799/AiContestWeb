"""AiContestWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from AiContestWeb import uaa
from AiContestWeb.contest.view import list_contest, retrieve_contest, create_contest, update_contest, delete_contest
from AiContestWeb.snippets import view

# Create a router and register our viewsets with it.
from AiContestWeb.uaa.view import UserViewSet, list_user, create_user, update_user, retrieve_user

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # All path related to CRUD user
    path('users/', list_user),
    path('users/<int:id>', retrieve_user),
    path('users/create', create_user),
    path('users/<int:id>/update', update_user),
    # All path related to CRUD user

    # All path related to CRUD contest
    path('contests/', list_contest),
    path('contests/<int:id>', retrieve_contest),
    path('contests/create', create_contest),
    path('contests/<int:id>/update', update_contest),
    path('contests/<int:id>/delete', delete_contest),
    # All path related to CRUD contest

    # Test
    path('snippets', view.snippet_list),
    # Test

    # Base
    path('', include(router.urls)),
    # Base

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
