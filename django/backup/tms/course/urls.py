from django.urls import path
from .views import GenerateScheduleView, GanttChartView, GenerateTrainingPlanView, TrainingPlanConfirmationView,TrainingPlanListView,GenerateLessonPlanView,ModuleDetailView

urlpatterns = [
    path('generate_schedule/<int:pk>/', GenerateScheduleView.as_view(), name='generate_schedule'),
    path('gantt_chart/<int:course_id>/', GanttChartView.as_view(), name='gantt_chart'),
  path('generate_training_plan/', GenerateTrainingPlanView.as_view(), name='generate_training_plan'),
    path('training_plan_confirmation/', TrainingPlanConfirmationView.as_view(), name='training_plan_confirmation'),
path('training_plan/<int:course_id>/', TrainingPlanListView.as_view(), name='training_plan_list'),
path('generate_lesson_plan/<int:module_id>/', GenerateLessonPlanView.as_view(), name='generate_lesson_plan'),
    path('module/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),

]



