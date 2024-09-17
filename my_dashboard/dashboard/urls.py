from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.attendance_dashboard, name='attendance_dashboard'),
 path('assign_tasks/', views.assign_tasks, name='assign_tasks'),
    path('task_schedule/', views.task_schedule_view, name='task_schedule_view'),
    path('edit_task/<int:schedule_id>/', views.edit_task, name='edit_task'),
path('assign_tasks/<int:batch_id>/', views.assign_tasks_to_batch, name='assign_tasks_to_batch'),
    path('batches/', views.batch_list_view, name='batch_list_view'),
]


