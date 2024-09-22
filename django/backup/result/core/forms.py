from django import forms
from .models import Submission, Activity

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'feedback']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'due_date']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'feedback']
