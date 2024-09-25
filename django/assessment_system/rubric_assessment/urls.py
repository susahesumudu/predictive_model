from django.urls import path
from . import views

app_name = 'rubric_assessment'


urlpatterns = [
    path('', views.rubric_list, name='rubric_list'),  # List all rubrics
    path('assess/<int:rubric_id>/', views.assess_student, name='assess_student'),  # Assess student for a rubric
    path('activities/', views.completed_activities, name='completed_activities'),  # List completed activities
    path('activities/grade/<int:activity_id>/', views.grade_activity, name='grade_activity'),  # Grade an activity
   path('students/', views.student_list, name='student_list'),  # List all students
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),  # View student details
path('activities/complete/<int:activity_id>/', views.mark_activity_completed, name='mark_activity_completed')

]

