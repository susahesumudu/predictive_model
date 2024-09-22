from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'deadline', 'duration_hours']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'duration_hours': forms.NumberInput(attrs={'min': 0, 'step': 0.5}),
        }

