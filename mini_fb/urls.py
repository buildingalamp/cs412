# File: urls.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: url file used to define url patterns and route urls

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView
from .views import CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView
from .views import UpdateStatusMessageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('profile/create', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status")
]