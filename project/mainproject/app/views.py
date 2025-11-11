from django.shortcuts import render, get_object_or_404, redirect
from .models import Class
# from django.http import HttpResponse
from .forms import ClassForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def get_class_context(user):
    context = {}
    classes = Class.objects.filter(author=user)
    
    day_of_the_week_list = ["月", "火", "水", "木", "金", "土"]
    # 授業を入れる配列[曜日][時限]
    class_list = [[None for _ in range(8)] for _ in range(6)]
    # 時限ごとに授業があるかどうかの配列
    exist_class_per_period_list = [False for _ in range(8)]
    exist_saturday_class = False
    max_period = 8
    
    for subject in classes:
        class_list[subject.day_of_the_week][subject.period - 1] = subject
        if subject.day_of_the_week == 5:  # 土曜日のクラスが存在するか確認
            exist_saturday_class = True
            
        exist_class_per_period_list[subject.period - 1] = True
            
    if not exist_saturday_class:
        # 土曜日に授業がない場合、配列から削除
        class_list.pop()
        
    # 4~8限目で授業がない場合、配列から削除
    for period in range(8, 4, -1):
        if exist_class_per_period_list[period - 1] == False:
            max_period = period - 1
            for subjects in class_list:
                subjects.pop()
        else:
            break
            
            
    
    context["class_list"] = class_list
    context["day_of_the_week_list"] = day_of_the_week_list
    context["exist_class_per_period_list"] = exist_class_per_period_list
    context["timetable_row"] = max_period
    if exist_saturday_class:
        context["timetable_column"] = 7
    else:
        context["timetable_column"] = 6
    context["period_range"] = range(1, max_period + 1)
    return context

@login_required
def index(request):
    context = get_class_context(request.user)
    if 'edit_mode' in request.GET and request.GET['edit_mode'] == 'on':
        context['is_editing'] = True
    return render(request, "app/index.html", context=context)

# ログインしていないユーザーがアクセスすると
# -> settings.LOGIN_URL にリダイレクトされます。

@login_required
def home_edit(request, id_day_of_week, id_period):
    context = get_class_context(request.user)
    
    if request.method == "POST":
        form = ClassForm(request.POST)
        
        if form.is_valid():
            class_form = form.save(commit=False)
            class_form.author = request.user
            class_form.save()
            # context.clear()
            
            # context = get_class_context()
            # context["form"] = ClassForm()
            # context["is_editing"] = True
            return redirect(reverse('app:index') + '?edit_mode=on')
        
        return render(request, "app/home-edit.html", {"form": ClassForm()}, context=context)
    
    elif request.method == "GET":
        initial_data = {
            "day_of_the_week": id_day_of_week - 1,
            "period": id_period,
        }
        form = ClassForm(initial=initial_data)
        context["form"] = form
        return render(request, "app/home-edit.html", context=context)

@require_POST
@login_required
def delete_class(request, class_id):
    subject = get_object_or_404(Class, pk=class_id)
    if subject.author != request.user:
        return redirect('app:index')
    subject.delete()
    messages.success(request, "授業を削除しました。")
    return redirect(reverse('app:index') + '?edit_mode=on')

    