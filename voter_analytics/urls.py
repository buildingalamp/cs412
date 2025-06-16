# File: urls.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: url file used to define url patterns and route urls

from django.urls import path
from . import views

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VoterListView.as_view(), name='home'),
    path(r'voters', views.VoterListView.as_view(), name='voters'),
    path(r'voters/<int:pk>', views.VoterDetailView.as_view(), name='voter_detail'),
]