# File: urls.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/23/2025
# Description: url file used to define url patterns and route urls

from django.urls import path
from .views import ProjectRegisterView, ProjectLoginView, ProjectLogoutView, ShowAllFightersView, ShowAllFightsView, ShowFighterView
from .views import ShowFightView, ShowFighterView, CreateFighterView, UpdateFighterView, CreateFightView, DeleteFightView, RateFightView

urlpatterns = [
    path('register/', ProjectRegisterView.as_view(), name='register'),
    path('login/', ProjectLoginView.as_view(), name='login'),
    path('logout/', ProjectLogoutView.as_view(), name='logout'),
    path('fighter/all', ShowAllFightersView.as_view(), name="show_all_fighters"),
    path('fighter/<int:pk>', ShowFighterView.as_view(), name="show_fighter"),
    path('fight/all', ShowAllFightsView.as_view(), name="show_all_fights"),
    path('fight/<int:pk>', ShowFightView.as_view(), name="show_fight"),
    path('fighter/create', CreateFighterView.as_view(), name="create_fighter"),
    path('fighter/<int:pk>/update', UpdateFighterView.as_view(), name="update_fighter"),
    path('fight/create_fight', CreateFightView.as_view(), name="create_fight"),
    path('fight/<int:pk>/delete_fight', DeleteFightView.as_view(), name="delete_fight"),
    path('fight/<int:pk>/rate_fight', RateFightView.as_view(),name="rate_fight"),
]