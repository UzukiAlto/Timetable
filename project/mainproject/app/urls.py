from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path("", views.index, name="index"),
    # path("<str:username>/edit/<int:id_day_of_week>/<int:id_period>/", views.home_edit, name="home_edit"),
    path("edit/<int:id_day_of_week>/<int:id_period>/", views.home_edit, name="home_edit"),
    path("delete/<int:class_id>/", views.delete_class, name="delete_class"),
]