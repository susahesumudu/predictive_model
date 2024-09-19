from django.urls import path
from predictions import views

urlpatterns = [
    path('student/<int:student_id>/', views.student_performance_view, name='student_performance'),
]

