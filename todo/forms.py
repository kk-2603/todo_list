# forms.py
from django import forms
from .models import Category, Task

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name']

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        label='Due Date and Time',
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']        
        