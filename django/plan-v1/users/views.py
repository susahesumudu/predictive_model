from django.urls import reverse_lazy
from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.db.models import Avg  # Import Avg for aggregation


def predict_student_performance(submissions):
    """
    Mock predictive model: this function will analyze student's performance and generate improvement suggestions.
    """
    total_submissions = submissions.count()
    total_graded = submissions.filter(marks__isnull=False).count()

    # Calculate average grade
    if total_graded > 0:
        average_grade = submissions.filter(marks__isnull=False).aggregate(avg_grade=Avg('marks'))['avg_grade']
    else:
        average_grade = 0

    suggestions = []

    # Based on average grades, generate suggestions
    if average_grade < 60:
        suggestions.append("Your performance is below average. Focus on revising the material and completing assignments on time.")
    elif 60 <= average_grade < 75:
        suggestions.append("You are doing okay, but there's room for improvement. Try to attend more classes and participate in discussions.")
    else:
        suggestions.append("Great job! Keep up the good work. Try to help others in group activities.")

    # If the student is missing submissions
    if total_submissions > total_graded:
        suggestions.append(f"You have {total_submissions - total_graded} ungraded submissions. Make sure to submit all tasks.")

    return suggestions



# 1. List Users
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

# 2. Create User
class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

# 3. Update User
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

# 4. Delete User
class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


from django.contrib.auth.models import Group
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# 1. List Groups
class GroupListView(ListView):
    model = Group
    template_name = 'users/group_list.html'
    context_object_name = 'groups'

# 2. Create Group
class GroupCreateView(CreateView):
    model = Group
    fields = ['name']
    template_name = 'users/group_form.html'
    success_url = reverse_lazy('group_list')

# 3. Update Group
class GroupUpdateView(UpdateView):
    model = Group
    fields = ['name']
    template_name = 'users/group_form.html'
    success_url = reverse_lazy('group_list')

# 4. Delete Group
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'users/group_confirm_delete.html'
    success_url = reverse_lazy('group_list')



#===========================Login =-===================



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        
        # Check for group membership and redirect accordingly
        if user.is_superuser:
            return '/admin/'  # Redirect admins to the Django admin page
        elif user.groups.filter(name="Staff").exists():
            return '/staff_dashboard/'  # Redirect staff to staff view
        elif user.groups.filter(name="Teacher").exists():
            return '/teacher_dashboard/'  # Redirect teachers to teacher view
        elif user.groups.filter(name="LabAssistant").exists():
            return '/lab_dashboard/'  # Redirect lab assistants
        elif user.groups.filter(name="Demo").exists():
            return '/demo_dashboard/'  # Redirect demo users
        elif user.groups.filter(name="Student").exists():
            return '/student_dashboard/'  # Redirect students to student view
        else:
            return '/'  # Default: home page or main dashboard


def staff_dashboard(request):
    return render(request, 'users/staff_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'users/teacher_dashboard.html')


from course.models import Submission

from django.shortcuts import render

import matplotlib.pyplot as plt
import base64
from io import BytesIO



def student_dashboard(request):
    # Fetch the student's submissions
    submissions = Submission.objects.filter(student=request.user)
    total_submissions = submissions.count()
    total_graded = submissions.filter(marks__isnull=False).count()
    total_ungraded = total_submissions - total_graded

    # Predictive model: generate suggestions for student improvement
    suggestions = predict_student_performance(submissions)

    # Prepare data for the pie chart (Grades per Activity)
    activities = [submission.activity.title for submission in submissions]
    grades = [submission.marks if submission.marks is not None else 0 for submission in submissions]

    # Breakdown of grades by range
    grade_ranges = {
        '90-100': sum(1 for g in grades if 90 <= g <= 100),
        '80-89': sum(1 for g in grades if 80 <= g < 90),
        '70-79': sum(1 for g in grades if 70 <= g < 80),
        '60-69': sum(1 for g in grades if 60 <= g < 70),
        'Below 60': sum(1 for g in grades if g < 60),
    }

    # Pie chart for grade breakdown by range
    plt.figure(figsize=(6, 6))  # Adjust size for the pie chart
    plt.pie(grade_ranges.values(), labels=grade_ranges.keys(), autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.
    plt.title('Grade Breakdown by Range')

    # Save the pie chart to a BytesIO object
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_pie_grades_breakdown = buffer.getvalue()
    buffer.close()

    # Encode the pie chart to base64
    pie_grades_breakdown_chart = base64.b64encode(image_pie_grades_breakdown).decode('utf-8')

    # Create a pie chart for graded vs ungraded submissions
    plt.figure(figsize=(6, 6))
    labels = ['Graded', 'Ungraded']
    sizes = [total_graded, total_ungraded]
    colors = ['#4CAF50', '#FF9999']
    explode = (0.1, 0)  # Explode the 'Graded' section slightly
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.

    # Save the pie chart to a BytesIO object
    buffer_pie = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer_pie, format='png')
    buffer_pie.seek(0)
    image_pie_png = buffer_pie.getvalue()
    buffer_pie.close()

    # Encode the pie chart to base64
    pie_chart = base64.b64encode(image_pie_png).decode('utf-8')

    return render(request, 'users/student_dashboard.html', {
        'submissions': submissions,
        'total_submissions': total_submissions,
        'total_graded': total_graded,
        'pie_grades_breakdown_chart': pie_grades_breakdown_chart,  # Grades breakdown by range
        'pie_chart': pie_chart,  # Graded vs ungraded submissions
        'suggestions': suggestions,  # Improvement suggestions from predictive model
    })








  






def lab_dashboard(request):
    return render(request, 'users/lab_dashboard.html')

def demo_dashboard(request):
    return render(request, 'users/demo_dashboard.html')




