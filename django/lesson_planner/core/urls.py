from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('submit-task/<int:activity_id>/', views.submit_work, name='submit_task'),
    path('plan-activities/<int:task_id>/', views.plan_activities, name='plan_activities'),
]

