from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView,UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, ProfileForm,UserRegistrationForm
from .models import Profile
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.contrib.auth.views import  LogoutView ,LoginView #
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'app.view_dashboard'
    template_name = 'dashboard.html'

   # Pass dynamic content to the dashboard
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile  # Assuming a UserProfile model exists
        context['notifications'] = ["Notification 1", "Notification 2", "Notification 3"]  # Example notifications
        context['progress'] = {
            'attended_classes': 10,
            'completed_assignments': 5,
            'next_class': 'Web Development',
        }
        return context




class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()  # Save the new user
        user_type = self.kwargs.get('user_type', 'Student')  # Get user_type from URL or set default

        # Ensure that the user doesn't already have a profile before creating one
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, user_type=user_type)
        
        login(self.request, user)  # Log the user in after registration
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

# Profile Update View (Manage your profile)
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Ensure the profile belongs to the logged-in user
        return self.request.user.profile

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Your login template

    def get_success_url(self):
        """This method gets called after a successful login."""
        user = self.request.user
        if user.is_superuser or user.is_staff:  # Check if the user is an admin or staff
            return '/admin/'  # Redirect to the Django admin page
        else:
            return '/accounts/dashboard/'




class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if user belongs to 'Teachers' or 'Students' group
        is_teacher = self.request.user.groups.filter(name="Teachers").exists()
        is_student = self.request.user.groups.filter(name="Students").exists()

        if is_teacher:
            context['role'] = 'Teacher'
            # Fetch additional data for teacher, e.g., pending tasks to review
        elif is_student:
            context['role'] = 'Student'
            # Fetch additional data for student, e.g., tasks to complete
        else:
            context['role'] = 'Unknown'

        return context

# Profile Edit View
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/profile_edit.html'  # Ensure this points to the correct template
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

# User login view (class-based)
class UserLoginView(LoginView):
    template_name = 'account/login.html'  # Customize this with your login template path

# User logout view (class-based)
class UserLogoutView(LogoutView):
    template_name = 'account/logged_out.html'  # Customize this with your logout template path

# Profile Detail View (View profile details)
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'

    def get_object(self):
        # Ensure the profile belongs to the logged-in user
        return self.request.user.profile



