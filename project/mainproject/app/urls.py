from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path("", views.index, name="index"),
    path("add_class/<str:username>/<int:id_day_of_week>/<int:id_period>/", views.home_edit, name="home_edit"),
    path("delete/<int:class_id>/<int:id_day_of_week>/<int:id_period>/", views.delete_class, name="delete_class"),
    path("class_edit/<int:class_id>/", views.class_edit, name="class_edit"),
    path("update/class_basic_info/", views.update_class_basic_info, name="update_class_basic_info"),
    path("update/memo/", views.update_memo, name="update_memo"),
    path("update/homework/", views.update_homework, name="update_homework"),
    path("delete/memo/", views.delete_memo, name="delete_memo"),
    path("delete/homework/", views.delete_homework, name="delete_homework"),
]