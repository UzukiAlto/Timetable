from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import Class, Homework, Memo, Class_cancellation
# from django.http import HttpResponse
from .forms import ClassForm, ClassBasicInfoForm, ClassScheduleForm, HomeworkForm, MemoForm
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
    
    if request.method == "POST":
        homework_form = HomeworkForm(request.POST)
        memo_form = MemoForm(request.POST)
        
        if 'submit-homework-form' in request.POST and homework_form.is_valid():
            new_homework = homework_form.save(commit=False)
            new_homework.class_model = subject
            new_homework.save()
            
        elif 'submit-memo-form' in request.POST and memo_form.is_valid():
            print("memo_form is valid")
            new_memo = memo_form.save(commit=False)
            new_memo.class_model = subject
            new_memo.save()
            
        return redirect('app:class_edit', class_id=class_id)
            
    if request.method == "GET":
        homework_items = subject.homework_set.all().order_by('deadline')
        memo_items = subject.memo_set.all().order_by('-created_at')
        
        # 授業名、教室名、教授名編集用フォーム
        class_basic_info_form = ClassBasicInfoForm(instance=subject)
        memos = []
        for memo_item in memo_items:
            memos.append({"item": memo_item, "form": MemoForm(initial={"content": memo_item.content})})
        
        homeworks = []
        for homework_item in homework_items:
            homeworks.append({"item": homework_item, "form": HomeworkForm(initial={
                "deadline": homework_item.deadline,
                "content": homework_item.content,
            })})
        homework_form = HomeworkForm()
        memo_add_form = MemoForm()
        
        context = {
            "subject": subject,
            "homeworks": homeworks,
            "memos": memos,
            "class_basic_info_form": class_basic_info_form,
            "homework_form": homework_form,
            "memo_form": memo_add_form,
            }
        return render(request, "app/class-edit.html", context=context)
    
def update_class_basic_info(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subject = get_object_or_404(Class, pk=data.get('id'))
            
            subject.class_name = data.get('class_name')
            subject.professor_name = data.get('professor_name')
            subject.classroom_name = data.get('classroom_name')
            subject.save()
            print("Class basic info updated successfully")
            # htmlではなくjsonを返す
            return JsonResponse({
                'status': 'success', 
                'new_subject': {
                    'class_name': subject.class_name,
                    'classroom_name': subject.classroom_name,
                    'professor_name': subject.professor_name
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def update_memo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            memo = get_object_or_404(Memo, pk=data.get('id'))
            
            memo.content = data.get('content')
            memo.save()
            
            # htmlではなくjsonを返す
            return JsonResponse({'status': 'success', 'new_content': memo.content})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def delete_memo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            memo_id = data.get('memo_id')
            memo = get_object_or_404(Memo, pk=memo_id)
            if memo.class_model.author != request.user:
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
            memo.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def update_homework(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            homework = get_object_or_404(Homework, pk=data.get('id'))
            homework.deadline = data.get('deadline')
            homework.content = data.get('content')
            homework.save()
            
            deadline_input = data.get('deadline').split('-')
            deadline_formatted_JP = f"{deadline_input[0]}年{deadline_input[1]}月{deadline_input[2]}日"
            
            # htmlではなくjsonを返す
            return JsonResponse({
                'status': 'success', 
                'new_deadline': deadline_formatted_JP,
                'new_content': homework.content
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def delete_homework(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            homework_id = data.get('id')
            homework = get_object_or_404(Homework, pk=homework_id)
            if homework.class_model.author != request.user:
                return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
            homework.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)