from django.urls import path
from .views import (
    CustomLoginView,
    AdminDashboardView,
    TeacherDashboardView,
    StudentDashboardView,
    StaffDashboardView,
    LabAssistantDashboardView,create_activity
)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Ensure this path exists

    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('lab-assistant/dashboard/', LabAssistantDashboardView.as_view(), name='lab_assistant_dashboard'),
  path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('teacher/task/<int:task_id>/create-activity/', create_activity, name='create_activity'),  # 
]




