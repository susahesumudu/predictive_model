from django import forms
from .models import Batch
from .models import Task



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'task_type', 'description', 'submission_deadline', 'batch']  # Add 'batch' field

    submission_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )





class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'teacher', 'students', 'course', 'start_date', 'end_date']
        widgets = {
            'students': forms.CheckboxSelectMultiple(),  # Multi-select for students
        }


