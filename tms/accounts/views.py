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



# Profile Edit View
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/profile_edit.html'  # Ensure this points to the correct template
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user



# Profile Detail View (View profile details)
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'

    def get_object(self):
        # Ensure the profile belongs to the logged-in user
        return self.request.user.profile

