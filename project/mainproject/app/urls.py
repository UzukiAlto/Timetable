from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/", views.home_edit, name="home_edit"),
]