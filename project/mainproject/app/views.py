from django.shortcuts import render
from .models import Class
# Create your views here.
from django.http import HttpResponse

def index(request):
    classes = Class.objects.all()
    context = {
        "classes": classes,
    }
    return render(request, "app/index.html", context=context)