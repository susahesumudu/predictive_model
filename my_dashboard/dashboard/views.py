from django.shortcuts import render, redirect
from .models import Metric, AttendanceRecord, Student, Task, Schedule, Batch
from django.db.models import Count, Q
import random

# Dashboard to show attendance
def attendance_dashboard(request):
    total_students = Student.objects.count()
    attendance_data = AttendanceRecord.objects.values('student__name').annotate(
        total_present=Count('status', filter=Q(status='Present')),
        total_absent=Count('status', filter=Q(status='Absent'))
    )

    return render(request, 'attendance/dashboard.html', {
        'total_students': total_students,
        'attendance_data': attendance_data
    })

# Dashboard view to show metrics
def dashboard_view(request):
    metrics = Metric.objects.all()
    return render(request, 'dashboard/dashboard.html', {'metrics': metrics})

# Generate tasks (exercises, assignments, assessments, and projects) if they do not exist
def generate_tasks():
    if not Task.objects.exists():
        tasks = [
            Task(name=f"Exercise {i+1}", task_type='Exercise') for i in range(50)
        ] + [
            Task(name=f"Assignment {i+1}", task_type='Assignment') for i in range(15)
        ] + [
            Task(name=f"Assessment {i+1}", task_type='Assessment') for i in range(5)
        ] + [
            Task(name=f"Project {i+1}", task_type='Project') for i in range(10)
        ]
        Task.objects.bulk_create(tasks)

# Assign tasks to students based on their batch
def assign_tasks_to_batch(request, batch_id):
    generate_tasks()  # Ensure tasks are generated before assignment

    batch = Batch.objects.get(id=batch_id)
    students = Student.objects.filter(batch=batch)

    for student in students:
        task_types = ['Exercise', 'Assignment', 'Assessment', 'Project']
        for task_type in task_types:
            task_list = Task.objects.filter(task_type=task_type)
            if task_list.exists():
                assigned_task = random.choice(task_list)
                Schedule.objects.create(student=student, task=assigned_task)

    return redirect('task_schedule_view')

# List all schedules with their assigned tasks
def task_schedule_view(request):
    schedules = Schedule.objects.all()
    return render(request, 'attendance/task_schedule.html', {'schedules': schedules})

# List all batches for task assignment
def batch_list_view(request):
    batches = Batch.objects.all()
    return render(request, 'attendance/batch_list.html', {'batches': batches})

# Randomly assign tasks to hardcoded students (for testing or demonstration)
def assign_tasks(request):
    generate_tasks()

    # List of hardcoded student names (in real life, fetch students from the database)
    student_names = ['Student A', 'Student B', 'Student C']

    for student_name in student_names:
        try:
            student = Student.objects.get(name=student_name)
        except Student.DoesNotExist:
            print(f"Student {student_name} does not exist in the database.")
            continue

        task_types = ['Exercise', 'Assignment', 'Assessment', 'Project']
        for task_type in task_types:
            task_list = Task.objects.filter(task_type=task_type)
            if task_list.exists():
                assigned_task = random.choice(task_list)
                Schedule.objects.create(student=student, task=assigned_task)

    return redirect('task_schedule_view')

# Allow a task in a schedule to be edited
def edit_task(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == 'POST':
        new_task_id = request.POST.get('task')
        new_task = Task.objects.get(id=new_task_id)
        schedule.task = new_task
        schedule.save()
        return redirect('task_schedule_view')

    tasks = Task.objects.all()
    return render(request, 'attendance/edit_task.html', {'schedule': schedule, 'tasks': tasks})

