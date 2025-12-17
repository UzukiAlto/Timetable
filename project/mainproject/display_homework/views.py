from django.shortcuts import render

# Create your views here.
def display_homework(request): 
    return render(request, "display_homework/display_homework.html") 