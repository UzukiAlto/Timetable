from django.shortcuts import render, get_object_or_404, redirect
from .models import Class
# from django.http import HttpResponse
from .forms import ClassForm
from .forms import ClassScheduleForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# 授業の情報を取得してコンテキストを作成
def get_class_context(user):
    context = {}
    
    classes = Class.objects.filter(author=user)
        
    # 授業を入れる配列[曜日][時限]
    # "exist_class_par_week":その週に授業があるかどうかのフラグ, "content":授業オブジェクト
    class_list = [[{"exist_class_par_week":True, "content":None} for _ in range(8)] for _ in range(6)]
    # 時限ごとに授業があるかどうかの配列
    exist_class_per_period_list = [False for _ in range(8)]
    for i in range(4):
        exist_class_per_period_list[i] = True  # 1~4限目は必ず授業があるものとする
        
    exist_saturday_class = False
    # 縦の最大値
    max_period = 8
    
    for subject in classes:
        for schedule in subject.class_schedule_set.all():
            # htmlに渡す配列に授業を格納
            class_list[schedule.day_of_the_week][schedule.period - 1]["content"] = subject
            if schedule.day_of_the_week == 5:  # 土曜日のクラスが存在するか確認
                exist_saturday_class = True
                
            exist_class_per_period_list[schedule.period - 1] = True
            
    # 土曜日に授業がない場合、存在フラグをFalseに
    if not exist_saturday_class:
        for subject in class_list[5]:
            subject["exist_class_par_week"] = False
        
    # 4~8限目で授業がない場合、縦の最大値を変更
    for period in range(8, 4, -1):
        if exist_class_per_period_list[period - 1] == False:
            max_period = period - 1
            # 存在フラグをFalseに
            for week in range(6):
                class_list[week][period - 1]["exist_class_par_week"] = False
        else:
            break
    
    context["class_list"] = class_list
    context["exist_class_per_period_list"] = exist_class_per_period_list
    context["exist_saturday_class"] = exist_saturday_class
    # 通常時に表示する縦の最大値
    context["timetable_row"] = max_period    
    # 通常時に表示する横の最大値
    if exist_saturday_class:
        context["timetable_column"] = 7
    else:
        context["timetable_column"] = 6
        
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
def home_edit(request, username, id_day_of_week, id_period):
    context = get_class_context(request.user)
    
    if request.method == "POST":
        schedule_data = ClassScheduleForm(request.POST, user=request.user)
        if not schedule_data.is_valid():
            return render_home_edit(request, context, id_day_of_week, id_period)

        save_new_class = schedule_data.cleaned_data.get('class_model') is None
        # スケジュールに既存の授業が紐づいていない場合、授業を新規作成
        if save_new_class:
            class_data = ClassForm(request.POST)
            
            if not class_data.is_valid() or class_data.cleaned_data.get('class_name') in ["", None]:
                return render_home_edit(request, context, id_day_of_week, id_period)
            
            # 授業情報を保存
                
            class_form = class_data.save(commit=False)
            class_form.author = request.user
            class_form.save()
            
            schedule_form = schedule_data.save(commit=False)
            schedule_form.class_model = class_form
                
            schedule_form.save()
            # 編集モードでindexにリダイレクト
            return redirect(reverse('app:index') + '?edit_mode=on')
                
        else:
            # 紐づける授業の情報がスケジュールにある場合、紐づけを行う
            class_data = get_object_or_404(Class, pk=schedule_data.cleaned_data.get('class_model').id)
            
            schedule_form = schedule_data.save(commit=False)
            schedule_form.class_model = class_data
                
            schedule_form.save()
            # 編集モードでindexにリダイレクト
            return redirect(reverse('app:index') + '?edit_mode=on')
            
    
    elif request.method == "GET":
        return render_home_edit(request, context, id_day_of_week, id_period)

# 授業追加画面を表示する処理をまとめた
def render_home_edit(request, context, id_day_of_week, id_period):
    context = get_class_context(request.user)
    class_form = ClassForm()    
    schedule_form = ClassScheduleForm(user = request.user, initial={
        "day_of_the_week": id_day_of_week - 1,
        "period": id_period,
    })
    context["class_form"] = class_form
    context["schedule_form"] = schedule_form
    
    return render(request, "app/home-edit.html", context=context)

@require_POST
@login_required
def delete_class(request, class_id, id_day_of_week, id_period):
    subject = get_object_or_404(Class, pk=class_id)
    if subject.author != request.user:
        return redirect('app:index')
    
    # 授業スケジュールが1つ以下の場合、授業自体を削除
    if subject.class_schedule_set.count() <= 1: 
        subject.delete()
    else:
        # 複数の時間に同じ授業が割り当てられている場合、該当の時間のみ削除
        schedule = get_object_or_404(
            subject.class_schedule_set,
            day_of_the_week=id_day_of_week,
            period=id_period
        )
        schedule.delete()
    return redirect(reverse('app:index') + '?edit_mode=on')

@login_required
def class_edit(request, class_id):
    subject = get_object_or_404(Class, pk=class_id)
    if subject.author != request.user:
        return redirect('app:index')
    context = {"subject": subject}
    return render(request, "app/class-edit.html", context=context)
