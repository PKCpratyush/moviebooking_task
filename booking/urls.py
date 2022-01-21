
from django.contrib import admin
from django.urls import path, include
from .views import MovieManagerAPI, UserLevel1API
import rest_framework

urlpatterns = [
    path('', UserLevel1API.as_view()),
    path('manager/', MovieManagerAPI.as_view())
]