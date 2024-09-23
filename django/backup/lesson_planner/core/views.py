from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Activity, Submission, Student
from .forms import SubmissionForm
from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request):
    # Ensure the user is a student
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('no_student_record')  # Or show an appropriate message

    tasks = Task.objects.prefetch_related('activities').all()

    context = {
        'student': student,
        'tasks': tasks,
    }
    return render(request, 'student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    # Ensure the user is a teacher
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('no_teacher_record')  # Or show an appropriate message

    tasks = Task.objects.all()

    context = {
        'teacher': teacher,
        'tasks': tasks,
    }
    return render(request, 'teacher_dashboard.html', context)

@login_required
def submit_work(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.activity = activity
            submission.save()
            return redirect('student_dashboard')
    else:
        form = SubmissionForm()

    return render(request, 'submit_task.html', {'activity': activity, 'form': form})

def no_student_record(request):
    return render(request, 'no_student_record.html', {'message': 'No student record found for your account.'})

def no_teacher_record(request):
    return render(request, 'no_teacher_record.html', {'message': 'No teacher record found for your account.'})

def no_student_record(request):
    return render(request, 'no_student_record.html', {'message': 'No student record found for your account.'})


@login_required
def plan_activities(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        name = request.POST['name']
        duration = request.POST['duration']
        description = request.POST['description']
        Activity.objects.create(task=task, name=name, duration=duration, description=description)
        return redirect('teacher_dashboard')
    return render(request, 'plan_activities.html', {'task': task})

