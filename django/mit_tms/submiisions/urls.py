# urls.py
from django.urls import path
from .views import SubmitExerciseView, ReviewExerciseListView, ReviewExerciseDetailView

urlpatterns = [
    path('submit-exercise/', SubmitExerciseView.as_view(), name='submit_exercise'),
    path('review-exercises/', ReviewExerciseListView.as_view(), name='review_exercises'),
    path('review-exercise/<int:pk>/', ReviewExerciseDetailView.as_view(), name='review_exercise'),
]

