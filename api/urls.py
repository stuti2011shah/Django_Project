from django.urls import path
import api.views as apiviews
import base.views as baseviews
import accounts.views as registerviews
from django.conf.urls import include

urlpatterns = [
    path('', apiviews.getRoutes, name="routes"),
]