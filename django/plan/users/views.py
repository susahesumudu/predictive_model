from django.urls import reverse_lazy
from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
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

def student_dashboard(request):
    return render(request, 'users/student_dashboard.html')

def lab_dashboard(request):
    return render(request, 'users/lab_dashboard.html')

def demo_dashboard(request):
    return render(request, 'users/demo_dashboard.html')
