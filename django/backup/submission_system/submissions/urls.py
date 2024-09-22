from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    # Task submission & scheduling
    path('submit/', views.submit_exercise, name='submit_exercise'),
    path('teacher/schedule/', views.schedule_task, name='schedule_task'),
    
    # Review exercises (Teacher)
    path('teacher/review/', views.review_exercises, name='review_exercises'),
    path('teacher/review/<int:exercise_id>/', views.review_exercise, name='review_exercise'),

    # Student status & search
        path('student/status/', views.student_status, name='student_status'),

    path('student/search/', views.student_search, name='student_search'),
]

