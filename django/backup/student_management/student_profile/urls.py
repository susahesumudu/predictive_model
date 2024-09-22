from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),

    path('create/', views.create_profile, name='create_profile'),
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('<int:pk>/edit/', views.update_profile, name='update_profile'),
]



