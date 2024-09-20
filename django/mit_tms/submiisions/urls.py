# urls.py
from django.urls import path
from .views import SubmitExerciseView, ReviewExerciseListView, ReviewExerciseDetailView, ScheduleTaskView,TeacherDashboardView, StudentDashboardView, UploadSubmissionView


urlpatterns = [
    path('submit-exercise/', SubmitExerciseView.as_view(), name='submit_exercise'),
    path('review-exercises/', ReviewExerciseListView.as_view(), name='review_exercises'),
    path('review-exercise/<int:pk>/', ReviewExerciseDetailView.as_view(), name='review_exercise'),
    path('schedule-task/', ScheduleTaskView.as_view(), name='schedule_task'),
        path('view_tasks_teacher/', TeacherDashboardView.as_view(), name='dashboard'),

 path('student-dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('upload-submission/<int:task_id>/', UploadSubmissionView.as_view(), name='upload_submission'),
]


