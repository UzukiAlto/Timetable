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