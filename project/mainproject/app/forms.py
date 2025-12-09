from django import forms
from .models import Class
from .models import Class_schedule, Homework, Memo

class ClassForm(forms.ModelForm):
    # selected_class = forms.ModelChoiceField()
    class Meta:
        model = Class
        # 入力する項目を設定
        fields = [
            'class_name',
            'professor_name',
            'classroom_name',
        ]
        widgets = {
            # TextInputウィジェットに、Bootstrapのクラス 'form-control' を設定
            'class_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '授業名を入力'}
            ),
            'professor_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '担当教授名を入力(任意)'}
            ),
            'classroom_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '教室名を入力(任意)'}
            ),
        }
        
    # フォームの初期化
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        # 必須を一時的に解除
        self.fields['class_name'].required = False

class ClassNameForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            'class_name',
            'professor_name',
            'classroom_name',
        ]

class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = Class_schedule
        fields = [
            'class_model',
            'day_of_the_week',
            'period',
        ]
        labels = {
            'class_model': '授業',
        }
        
        widgets = {
            'class_model': forms.Select(
                attrs={'class': 'form-select'} 
            ),
            'day_of_the_week': forms.HiddenInput(),
            'period': forms.HiddenInput(),
        }
        
    # フォームの初期化
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user is not None:
            # 表示する授業をユーザーごとにフィルタリング
            self.fields['class_model'].queryset = Class.objects.filter(author=user)
            # 必須を一時的に解除
            self.fields['class_model'].required = False
            
            
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = [
            'deadline',
            'content',
        ]
        
        widgets = {
            'deadline': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '宿題の内容を入力'}
            ),
        }
        
class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = [
            'content',
        ]        
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'メモの内容を入力'}
            ),
        }