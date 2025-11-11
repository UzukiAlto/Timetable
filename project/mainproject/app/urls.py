from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<int:id_day_of_week>/<int:id_period>/", views.home_edit, name="home_edit"),
    path("delete/<int:class_id>/", views.delete_class, name="delete_class"),
]