from django.urls import path
from .views import UserRegisterView, ProfileUpdateView, DashboardView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

]

