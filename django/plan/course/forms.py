# forms.py
from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_file']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'feedback']



from .models import GradingRubric

class GradingRubricForm(forms.ModelForm):
    class Meta:
        model = GradingRubric
        fields = ['criteria', 'description', 'max_points', 'points_awarded']

