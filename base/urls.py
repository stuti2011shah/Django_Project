from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('createteam/', views.createteam, name='createteam'),
    path('addmember/', views.addmember, name='addmember'),
    path('acceptinvite/<str:teamname>/', views.acceptinvite, name='acceptinvite'),
    path('rejectinvite/<str:teamname>/', views.rejectinvite, name='rejectinvite'),
    path('teams/', views.teams, name='teams'),
    path('team/<int:id>/', views.team, name='team'),
    path('searchhackathon/', views.searchhackathon, name='searchhackathon'),
    path('uhackathon/<str:hack>/', views.register_hackathon, name='uhackathon'),
    path('tags/', views.tags, name='tags'),
    path('organization/<str:name>/', views.create_hackathon, name='organization'),
    path('createhackathon/<str:name>/',views.hackathonform,name='hackathonform'),
    path('createteamform/<str:username>/',views.createteamform,name='createteamform'),
    path('uhackathonform/<str:hack>/', views.register_hackathonform, name='uhackathonform'),
    path('project/', views.project, name='project'),
]