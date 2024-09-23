# urls.py
from django.urls import path
from .views import (
    #Home Views
        HomePageView, 


    # Course views
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    
    # Module views
    ModuleListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, ModuleDeleteView,
    
    # Task views
    TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    
    # Activity views
    ActivityListView, ActivityDetailView, ActivityCreateView, ActivityUpdateView, ActivityDeleteView,SubmissionCreateView, SubmissionGradeView,RubricCreateView, RubricUpdateView,
)


urlpatterns = [
    # Home url
        path('', HomePageView.as_view(), name='home'),



    # Course URLs
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/new/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # Module URLs
    path('modules/', ModuleListView.as_view(), name='module_list'),
    path('modules/new/', ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),
    path('modules/<int:pk>/edit/', ModuleUpdateView.as_view(), name='module_edit'),
    path('modules/<int:pk>/delete/', ModuleDeleteView.as_view(), name='module_delete'),

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/new/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    # Activity URLs
    path('activities/', ActivityListView.as_view(), name='activity_list'),
    path('activities/new/', ActivityCreateView.as_view(), name='activity_create'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity_detail'),
    path('activities/<int:pk>/edit/', ActivityUpdateView.as_view(), name='activity_edit'),
    path('activities/<int:pk>/delete/', ActivityDeleteView.as_view(), name='activity_delete'),
    path('activities/<int:pk>/submit/', SubmissionCreateView.as_view(), name='submit_activity'),
    path('submissions/<int:pk>/grade/', SubmissionGradeView.as_view(), name='grade_submission'),


    path('activities/<int:pk>/rubric/new/', RubricCreateView.as_view(), name='rubric_create'),
    path('rubric/<int:pk>/edit/', RubricUpdateView.as_view(), name='rubric_edit'),


]


