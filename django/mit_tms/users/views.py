from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, f"Account created for {username}!")
        return redirect(self.success_url)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_form'] = UserUpdateForm(instance=self.request.user)
        context['p_form'] = self.get_form(self.get_form_class())
        return context

    def form_valid(self, form):
        u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        p_form = self.get_form(self.get_form_class())
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(self.request, 'Your profile has been updated!')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data())

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['groups'] = user.groups.all()  # Get all groups the user belongs to
        return context

