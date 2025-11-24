from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path("", views.index, name="index"),
    path("add_class/<str:username>/<int:id_day_of_week>/<int:id_period>/", views.home_edit, name="home_edit"),
    path("delete/<int:class_id>/<int:id_day_of_week>/<int:id_period>/", views.delete_class, name="delete_class"),
    path("class_edit/<int:class_id>/", views.class_edit, name="class_edit"),
]