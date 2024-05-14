from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Type your task title'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Describe your task details'}),
            'is_important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
        }