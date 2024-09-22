from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def student_status(request):
    # Get the student name from the query parameters
    student_name = request.GET.get('student_name', '')

    # Fetch exercises only for the student with the specified name
    exercises = Exercise.objects.filter(student_name=student_name)

    # If no exercises are found, handle that case
    if not exercises.exists():
        message = "No submissions found for the student."
    else:
        message = ""

    # Pass the filtered exercises to the template
    return render(request, 'submissions/student_status.html', {'exercises': exercises, 'message': message, 'student_name': student_name})

@login_required
def student_search(request):
    return render(request, 'submissions/status_search.html')

# Check if the user is a teacher
def is_teacher(user):
    return user.groups.filter(name='Teachers').exists()

# Check if the user is a student
def is_student(user):
    return user.groups.filter(name='Students').exists()

# Dashboard view - redirects based on user role

# Teacher dashboard - scheduling and review
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, 'submissions/teacher_dashboard.html')

# Schedule a task (Teacher)
@user_passes_test(is_teacher)
def schedule_task(request):
    if request.method == "POST":
        title = request.POST['title']
        task_type = request.POST['task_type']
        description = request.POST['description']
        submission_deadline = timezone.make_aware(timezone.datetime.strptime(request.POST['submission_deadline'], "%Y-%m-%dT%H:%M"))

        task = Task(title=title, task_type=task_type, description=description, submission_deadline=submission_deadline)
        task.save()
        return redirect('schedule_task')

    return render(request, 'submissions/schedule_task.html')

# Review exercises (Teacher)
@user_passes_test(is_teacher)
def review_exercises(request):
    exercises = Exercise.objects.filter(status="Pending")
    return render(request, 'submissions/review_exercises.html', {'exercises': exercises})

@user_passes_test(is_teacher)
def review_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if request.method == "POST":
        exercise.teacher_feedback = request.POST['teacher_feedback']
        exercise.grade = request.POST['grade']
        exercise.status = 'Reviewed'
        exercise.save()
        return redirect('review_exercises')

    return render(request, 'submissions/review_exercise.html', {'exercise': exercise})

# Student dashboard - view tasks and submit work
@user_passes_test(is_student)
def student_dashboard(request):
    tasks = Task.objects.order_by('submission_deadline')
    return render(request, 'submissions/student_dashboard.html', {'tasks': tasks})

# Submit an exercise (Student)
@user_passes_test(is_student)
def submit_exercise(request):
    tasks = Task.objects.all()  # Fetch all tasks

    if request.method == "POST":
        student_name = request.POST['student_name']
        task_id = request.POST['task_id']
        task = Task.objects.get(id=task_id)
        submission_time = timezone.now()

        # Determine if submission is on time or late
        completed_on_time = "Late" if submission_time > task.submission_deadline else "On Time"

        # Create the exercise
        new_exercise = Exercise(
            student_name=student_name,
            exercise_title=task.title,
            submission_time=submission_time,
            completed_on_time=completed_on_time,
            level_of_completion=request.POST['level_of_completion'],
            quality_of_work=request.POST['quality_of_work'],
            learning_outcome=request.POST['learning_outcome'],
            challenges=request.POST.get('challenges', ''),
        )
        new_exercise.save()
        return redirect('submit_exercise')

    return render(request, 'submissions/submit_exercise.html', {'tasks': tasks})

# Student status view (for checking submitted exercises)
@login_required
def dashboard(request):
    is_teacher = request.user.groups.filter(name="Teachers").exists()
    is_student = request.user.groups.filter(name="Students").exists()

    if is_teacher:
        # Fetch exercises to review for the teacher
        exercises = Exercise.objects.filter(status="Pending")
        context = {
            'is_teacher': True,
            'exercises': exercises
        }
    elif is_student:
        # Fetch tasks for the student
        tasks = Task.objects.order_by('submission_deadline')
        context = {
            'is_student': True,
            'tasks': tasks
        }
    else:
        # If the user is neither a teacher nor a student, show a generic dashboard
        context = {}

    return render(request, 'submissions/dashboard.html', context)
