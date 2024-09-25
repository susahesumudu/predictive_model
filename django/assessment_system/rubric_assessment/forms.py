from django import forms
from .models import Assessment, Student, Criteria

class AssessmentForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Select Student")

    class Meta:
        model = Assessment
        fields = ['student']

    def __init__(self, *args, **kwargs):
        rubric = kwargs.pop('rubric', None)
        super(AssessmentForm, self).__init__(*args, **kwargs)
        if rubric:
            # Dynamically create fields for each criteria under the rubric
            for criteria in Criteria.objects.filter(rubric=rubric):
                self.fields[criteria.name] = forms.IntegerField(
                    label=f"{criteria.name} (Max: {criteria.max_points})",
                    max_value=criteria.max_points,
                    min_value=0
                )
    
    def calculate_total_score(self):
        total_score = 0
        for field_name in self.fields:
            if isinstance(self.fields[field_name], forms.IntegerField):
                total_score += self.cleaned_data[field_name]
        return total_score

