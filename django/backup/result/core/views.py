from django.shortcuts import render, get_object_or_404, redirect
from .models import Activity, Submission, Prediction, Student, Task, Attendance
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .forms import SubmissionForm, GradeForm
from .ml_model import predict_pass_fail  # Assume you have your prediction model logic here
from datetime import date
from django.contrib.auth.decorators import login_required


from .models import Activity, Teacher
from .forms import ActivityForm

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def form_valid(self, form):
        # Add custom behavior here if needed
        return super().form_valid(form)


@login_required
def review_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')  # Redirect to dashboard after reviewing
    else:
        form = GradeForm(instance=submission)

    return render(request, 'review_submission.html', {'form': form})


@login_required
def schedule_activity(request, activity_id=None):
    teacher = get_object_or_404(Teacher, user=request.user)

    # If editing an existing activity, fetch it
    if activity_id:
        activity = get_object_or_404(Activity, id=activity_id, teacher=teacher)
    else:
        activity = None

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            new_activity = form.save(commit=False)
            new_activity.teacher = teacher
            new_activity.save()
            return redirect('teacher_dashboard')  # Redirect to dashboard after saving
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'schedule_activity.html', {'form': form})



@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)  # Get the teacher linked to the logged-in user
    activities = Activity.objects.filter(teacher=teacher)  # Get activities assigned to this teacher
    submissions = Submission.objects.filter(activity__teacher=teacher)  # Get submissions linked to this teacher's activities

    context = {
        'teacher': teacher,
        'activities': activities,
        'submissions': submissions,
    }
    
    return render(request, 'teacher_dashboard.html', context)

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('no_student_record')  # Redirect or handle the case where no student record exists

    prediction = Prediction.objects.filter(student=student).first()
    feedbacks = Submission.objects.filter(student=student).values('feedback')

    return render(request, 'dashboard.html', {
        'student': student,
        'prediction': prediction,
        'feedbacks': feedbacks
    })

def no_student_record(request):
    return render(request, 'no_student_record.html', {'message': 'No student record found for your account.'})


# Track attendance based on RFID
@login_required
def track_attendance(request, rfid):
    try:
        student = Student.objects.get(rfid_tag=rfid)
        Attendance.objects.create(student=student, date=date.today(), present=True)
        return JsonResponse({'message': 'Attendance recorded'}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({'message': 'Student not found'}, status=404)

# Submit work for a specific activity
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
            submission.task = activity.task  # Assuming the activity is linked to a task
            submission.save()
            return redirect('student_dashboard')
    else:
        form = SubmissionForm()

    return render(request, 'submit_task.html', {'activity': activity, 'form': form})

# Review submission by the teacher (assign marks and feedback)
@login_required
def review_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    teacher = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.graded = True
            submission.save()

            # Recalculate student's overall marks
            student = submission.student
            student.total_marks = calculate_total_marks(student)  # Define this method
            student.save()

            # Update student's prediction (optional)
            prediction = predict_pass_fail(student.id)
            Prediction.objects.update_or_create(
                student=student,
                defaults={'predicted_pass': prediction['pass'], 'feedback': prediction['feedback']}
            )
            return redirect('teacher_dashboard')
    else:
        form = GradeForm(instance=submission)

    return render(request, 'assign_grade.html', {'submission': submission, 'form': form})

# Student dashboard to view progress and feedback
@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    prediction = Prediction.objects.filter(student=student).first()
    feedbacks = Submission.objects.filter(student=student).values('feedback')

    return render(request, 'dashboard.html', {
        'student': student,
        'prediction': prediction,
        'feedbacks': feedbacks
    })

# View to submit a task
@login_required
def student_task_submission(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.task = task
            submission.save()
            return redirect('student_dashboard')
    else:
        form = SubmissionForm()

    return render(request, 'submit_task.html', {'task': task, 'form': form})

# Teacher's view to assign grades and feedback
@login_required
def assign_grade(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard', student_id=submission.student.id)
    else:
        form = GradeForm(instance=submission)

    return render(request, 'assign_grade.html', {'form': form})


@login_required
def student_task_submission(request, task_id):
    task = get_object_or_404(Task, id=task_id)  # This line throws the 404 if the task doesn't exist
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.task = task
            submission.save()
            return redirect('student-dashboard')
    else:
        form = SubmissionForm()

    return render(request, 'submit_task.html', {'task': task, 'form': form})

