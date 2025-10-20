from django.shortcuts import render, get_object_or_404, redirect
from .models import Class
from django.http import HttpResponse
from .forms import ClassForm
from django.contrib.auth.decorators import login_required

def index(request):
    classes = Class.objects.all()
    context = {
        "classes": classes,
    }
    return render(request, "app/index.html", context=context)

@login_required
def home_edit(request):
    classes = Class.objects.all()
    context = {"classes": classes}
    
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            class_form = form.save(commit=False)
            class_form.author = request.user
            class_form.save()
            return render(request, "app/home-edit.html", context=context)
        return render(request, "app/home-edit.html", {"form": ClassForm()}, context=context)
    elif request.method == "GET":
        form = ClassForm()
        context["form"] = form
        return render(request, "app/home-edit.html", context=context)