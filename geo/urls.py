from django.urls import path
from . import views

urlpatterns = [
    path("", views.geo_home, name="geo-home"),
]