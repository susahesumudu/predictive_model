# project's main urls.py (e.g., project/urls.py)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from users.views import staff_dashboard, teacher_dashboard, student_dashboard, lab_dashboard, demo_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include app URLs
    path('courses/', include('course.urls')),  # Course app URLs under /courses/
    path('users/', include('users.urls')),  # User-related URLs
    
    # Dashboard views for different user roles
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('lab_dashboard/', lab_dashboard, name='lab_dashboard'),
    path('demo_dashboard/', demo_dashboard, name='demo_dashboard'),

    # Login and Logout views (ensure the templates exist in the correct path)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Redirect after logout

    # Uncomment this if you want the home page to redirect to login
    path('', TemplateView.as_view(template_name='registration/login.html'), name='home'),
]

