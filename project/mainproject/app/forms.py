from django import forms
from .models import Class

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            'class_name',
            'professor_name',
            'classroom_name',
            'day_of_the_week',
            'period',
        ]
        widgets = {
            # 1. テキスト入力フィールド (class_name, professor_name, classroom_name)
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
            'day_of_the_week': forms.Select(
                attrs={'class': 'form-select'} # Bootstrap 5 のドロップダウン用クラス
            ),
            'period': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }