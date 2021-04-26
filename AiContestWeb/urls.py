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
from AiContestWeb.attendee.view import list_attendee, retrieve_attendee, create_attendee, update_attendee, \
    delete_attendee
from AiContestWeb.contest.view import list_contest, retrieve_contest, create_contest, update_contest, delete_contest
# Create a router and register our viewsets with it.
from AiContestWeb.uaa.view import UserViewSet, list_user, create_user, update_user, retrieve_user, login

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
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

    # All path related to CRUD attendee
    path('contests/<int:contest_id>/attendees/create', create_attendee),
    path('attendees/', list_attendee),
    path('attendees/<int:id>', retrieve_attendee),
    path('attendees/<int:id>/update', update_attendee),  # Not work for now
    path('attendees/<int:id>/delete', delete_attendee),
    # All path related to CRUD attendee

    # login, register
    path('login', login),
    path('register', create_user),
    # login, register

    # Base
    path('', include(router.urls)),
    # Base

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
