from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from google.oauth2 import id_token
from google.auth.transport import requests
import json

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("app:index")
        
        else:
            return render(request, "accounts/signup.html", {"form": form})
    
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "accounts/signup.html", {"form": form})

CLIENT_ID = "845944346746-uvhtfg0gosl5e352ckh4et9vrp2k94lg.apps.googleusercontent.com"

def google_login(request):
    """GoogleサインインのIDトークンを検証し、ログイン処理を行う"""
    if request.method == 'POST':
        token = request.POST.get('idtoken')
        
        try:
            # Googleのトークンを検証
            # clock_skew_in_seconds=10 を追加して、PCの時刻が多少ずれていても許容するようにします
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), CLIENT_ID, clock_skew_in_seconds=10)

            # 検証成功。ユーザー情報を取得
            email = idinfo['email']
            
            # ユーザーの取得または作成
            # ここではメールアドレスをユーザー名として使用します
            # 既存ユーザーがいれば取得、いなければ新規作成
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            
            # Djangoのログイン処理を実行
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return JsonResponse({'status': 'success'})
            
        except ValueError as e:
            # トークンが無効な場合
            print(f"Google token verification error: {e}")  # エラー内容をコンソールに出力
            return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
