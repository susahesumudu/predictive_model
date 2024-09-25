from django.shortcuts import render, redirect
from .models import Rubric, Criteria, Assessment
from .forms import AssessmentForm
from .models import Activity



def assess_student(request, rubric_id):
    rubric = get_object_or_404(Rubric, pk=rubric_id)
    if request.method == 'POST':
        form = AssessmentForm(request.POST, rubric=rubric)
        if form.is_valid():
            total_score = form.calculate_total_score()
            assessment = form.save(commit=False)
            assessment.total_score = total_score
            assessment.rubric = rubric
            assessment.save()
            return redirect('rubric_assessment:rubric_list')
    else:
        form = AssessmentForm(rubric=rubric)
    
    return render(request, 'rubric_assessment/assess_student.html', {'form': form, 'rubric': rubric})



# View to show all completed activities of a student
def completed_activities(request):
    activities = Activity.objects.filter(completed=True)
    return render(request, 'rubric_assessment/completed_activities.html', {'activities': activities})

# View to assign grades to a completed activity
def grade_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    rubric = activity.rubric  # Use the rubric linked to the activity
    
    if request.method == 'POST':
        form = AssessmentForm(request.POST, rubric=rubric)
        if form.is_valid():
            total_score = form.calculate_total_score()
            assessment = form.save(commit=False)
            assessment.student = activity.student  # Assign the correct student
            assessment.total_score = total_score
            assessment.rubric = rubric
            assessment.save()
            return redirect('rubric_assessment:completed_activities')
    else:
        form = AssessmentForm(rubric=rubric)
    
    return render(request, 'rubric_assessment/grade_activity.html', {'form': form, 'activity': activity})

from django.shortcuts import render, get_object_or_404
from .models import Student

# List all students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'rubric_assessment/student_list.html', {'students': students})

# Display individual student details
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'rubric_assessment/student_detail.html', {'student': student})

from .models import Student, Assessment

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    assessments = Assessment.objects.filter(student=student)
    return render(request, 'rubric_assessment/student_detail.html', {'student': student, 'assessments': assessments})


def mark_activity_completed(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.mark_completed()
    return redirect('rubric_assessment:completed_activities')


from django.shortcuts import render
from .models import Rubric

def rubric_list(request):
    rubrics = Rubric.objects.all()
    return render(request, 'rubric_assessment/rubric_list.html', {'rubrics': rubrics})


