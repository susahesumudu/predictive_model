from django.urls import path
from . import views

urlpatterns = [
    path('mark_attendance/<int:session_id>/', views.mark_attendance, name='mark_attendance'),
    path('attendance_report/<int:session_id>/', views.attendance_report, name='attendance_report'),
]

