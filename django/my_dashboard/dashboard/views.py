
from .models import Metric
from .models import AttendanceRecord, Student
from django.db.models import Count
from django.db.models import Count, Q  # Import models from Django's ORM
from django.shortcuts import render, redirect
from .models import Task, Schedule
import random

def attendance_dashboard(request):
    # Fetch attendance data
    total_students = Student.objects.count()
    attendance_data = AttendanceRecord.objects.values('student__name').annotate(
        total_present=Count('status', filter=Q(status='Present')),
        total_absent=Count('status', filter=Q(status='Absent'))
    )
    
    return render(request, 'attendance/dashboard.html', {
        'total_students': total_students,
        'attendance_data': attendance_data
    })




def dashboard_view(request):
    metrics = Metric.objects.all()
    return render(request, 'dashboard/dashboard.html', {'metrics': metrics})





def generate_tasks():
    """Create tasks based on predefined types."""
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

def assign_tasks(request):
    """Randomly assign tasks to students."""
    if not Task.objects.exists():
        generate_tasks()

    students = ['Student A', 'Student B', 'Student C']  # Replace with real students

    for student in students:
        # Get all task types
        task_types = ['Exercise', 'Assignment', 'Assessment', 'Project']
        for task_type in task_types:
            task_list = Task.objects.filter(task_type=task_type)
            assigned_task = random.choice(task_list)  # Randomly assign a task

            # Assign task to the schedule
            Schedule.objects.create(student=student, task=assigned_task)

    return redirect('task_schedule_view')  # Redirect to schedule view after assignment

def task_schedule_view(request):
    """Display the scheduled tasks and allow editing."""
    schedules = Schedule.objects.all()
    return render(request, 'attendance/task_schedule.html', {'schedules': schedules})

def edit_task(request, schedule_id):
    """Allow the user to edit a task for a given schedule."""
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == 'POST':
        new_task_id = request.POST.get('task')
        new_task = Task.objects.get(id=new_task_id)
        schedule.task = new_task
        schedule.save()
        return redirect('task_schedule_view')

    tasks = Task.objects.all()
    return render(request, 'attendance/edit_task.html', {'schedule': schedule, 'tasks': tasks})

