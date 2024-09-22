from django.shortcuts import render

from .models import Course, Module, Task, Activity, TrainingPlan
import random


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ActivityForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView

from django.contrib.auth.models import Group

# Custom login view to redirect users based on their group
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Your login template

    def get_success_url(self):
        user = self.request.user

        if user.groups.filter(name='Admin').exists():
            return '/admin/dashboard/'
        elif user.groups.filter(name='Teacher').exists():
            return '/teacher/dashboard/'
        elif user.groups.filter(name='Student').exists():
            return '/student/dashboard/'
        elif user.groups.filter(name='Staff').exists():
            return '/staff/dashboard/'
        elif user.groups.filter(name='Lab Assistant').exists():
            return '/lab-assistant/dashboard/'
        else:
            return '/login/'




def create_activities():
    courses = {
        "Web Development": {
            "modules": ["HTML & CSS", "JavaScript", "Backend Development"],
            "tasks": {
                "HTML & CSS": ["Learn HTML", "Learn CSS", "Responsive Design"],
                "JavaScript": ["Basic JS Syntax", "DOM Manipulation", "AJAX"],
                "Backend Development": ["Setting up Flask", "Database Integration", "API Development"],
            }
        },
        "Data Science": {
            "modules": ["Introduction to Python", "Statistics", "Machine Learning"],
            "tasks": {
                "Introduction to Python": ["Python Basics", "Data Structures", "Functions and OOP"],
                "Statistics": ["Descriptive Stats", "Probability", "Hypothesis Testing"],
                "Machine Learning": ["Supervised Learning", "Unsupervised Learning", "Neural Networks"],
            }
        }
    }

    activity_types = ["exercise", "work_project", "assignment", "assessment", "lecture", "discussion"]
    session_types = ["theory", "practical"]

    for course_name, course_data in courses.items():
        course = Course.objects.create(name=course_name, description=f"Course on {course_name}")
        
        for module_name in course_data["modules"]:
            module = Module.objects.create(course=course, title=module_name)

            for task_name in course_data["tasks"][module_name]:
                task = Task.objects.create(module=module, title=task_name, description=f"{task_name} description")
                
                for i in range(10):  # Create 10 activities per task
                    Activity.objects.create(
                        task=task,
                        title=f"{task_name} Activity {i + 1}",
                        activity_type=random.choice(activity_types),
                        session_type=random.choice(session_types),
                        duration_hours=round(random.uniform(1, 4), 1)  # Random duration between 1 to 4 hours
                    )


@login_required
def create_activity(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.task = task
            activity.save()
            return redirect('teacher_dashboard')  # Redirect back to the teacher's dashboard
    return redirect('teacher_dashboard')  # Handle invalid form case

# Base dashboard view
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

# Admin Dashboard
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

# Teacher Dashboard
class TeacherDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'teacher_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Teacher').exists()



class TeacherDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'teacher_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Teacher').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming the teacher is assigned to a specific training plan
        # Fetch tasks related to the teacher's training plan
        teacher_training_plan = TrainingPlan.objects.filter(batch__teacher__user=self.request.user).first()
        tasks = teacher_training_plan.tasks.all() if teacher_training_plan else []

        context['tasks'] = tasks
        context['training_plan'] = teacher_training_plan
        return context




# Student Dashboard
class StudentDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'student_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Student').exists()

# Staff Dashboard
class StaffDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'staff_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

# Lab Assistant Dashboard
class LabAssistantDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'lab_assistant_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Lab Assistant').exists()



