
from django.urls import path

from .views import RegisterView, ProfileView,CustomLogoutView ,CustomLoginView,ProfileEditView,DashboardView




urlpatterns = [
    path('register/<str:user_type>/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
       path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('logout/', CustomLogoutView.as_view(), name='logout'),


]



