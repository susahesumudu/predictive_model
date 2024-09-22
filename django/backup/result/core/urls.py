from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # URL for student submission
path('submit-task/<int:task_id>/', views.student_task_submission, name='submit-task'),

    path('dashboard/', views.student_dashboard, name='student-dashboard'),  # No student_id needed here

    # URL for teacher to assign grade
    path('assign-grade/<int:submission_id>/', views.assign_grade, name='assign-grade'),

    # URL for student dashboard
   

    # URL for teacher attendance tracking (using RFID)
    path('track-attendance/<str:rfid_tag>/', views.track_attendance, name='track-attendance'),

    path('no-student/', views.no_student_record, name='no_student_record'),
 path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('schedule-activity/', views.schedule_activity, name='schedule_activity'),  # For scheduling activities
    path('schedule-activity/<int:activity_id>/', views.schedule_activity, name='schedule_activity_with_id'),  # Edit existing activity
    path('review-submission/<int:submission_id>/', views.review_submission, name='review_submission'),  # For reviewing submissions


    # Login page
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # Logout page

path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    

]




