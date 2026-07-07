from django.urls import path
from . import views

urlpatterns = [
    path("", views.destination_home, name="destination-home"),
]