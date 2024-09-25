from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView,GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView,CustomLoginView
from django.contrib.auth import views as auth_views


    


urlpatterns = [

#users 
    path('register/', UserCreateView.as_view(), name='register'),  # User registration
    path('users/', UserListView.as_view(), name='user_list'),  # List users
    path('users/new/', UserCreateView.as_view(), name='user_create'),  # Create user
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),  # Update user
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),  # Delete user



#user Groups

    path('groups/', GroupListView.as_view(), name='group_list'),  # List groups
    path('groups/new/', GroupCreateView.as_view(), name='group_create'),  # Create group
    path('groups/<int:pk>/edit/', GroupUpdateView.as_view(), name='group_edit'),  # Update group
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),  


#login
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]


