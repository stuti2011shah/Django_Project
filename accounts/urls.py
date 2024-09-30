from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from accounts import views


urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logoutv, name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('loginOrg/', views.loginOrg, name='loginOrg'),
    path('registerOrg/', views.registerOrg, name='registerOrg'),
]