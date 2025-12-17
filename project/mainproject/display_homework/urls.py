from django.urls import path
from .views import display_homework
 
urlpatterns = [
    path("display_homework", display_homework, name="display_homework"),
]
