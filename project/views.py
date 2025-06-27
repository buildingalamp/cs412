# File: views.spy
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: views file used to define the view classes

import django.views.generic
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .models import *
from .forms import *
# Create your views here.

class ProjectRegisterView(CreateView):
    """View to register a new user"""

    form_class = UserCreationForm
    template_name = "project/register.html"
    success_url = reverse_lazy("login")

class ProjectLoginView(LoginView):
    """Login view"""

    template_name = "project/login.html"

    def get_success_url(self):
        """Necessary to define login redirect url specific to project webapp"""
        return reverse_lazy("show_all_fighters")


class ProjectLogoutView(LogoutView):
    """Logout view"""

    next_page = reverse_lazy("show_all_fighters")

class ShowAllFightersView(ListView):
    """View class to show all fighters. Inherits from ListView"""

    model = Fighter
    template_name = "project/show_all_fighters.html"
    context_object_name = "fighters"

    def get_context_data(self, **kwargs):
        """Weight classes context data for show_all_fighters.html to show by fighters by weight class"""

        context = super().get_context_data(**kwargs)
        context['weight_classes'] = WeightClass.objects.all()
        return context

class ShowFighterView(DetailView):
    """View class to show a single Fighter's page. Inherits from DetailView"""

    model = Fighter
    template_name = "project/show_fighter.html"
    context_object_name = "fighter"

class ShowAllFightsView(ListView):
    """View class to show all fights. Inherits from ListView"""

    model = Fight
    template_name = "project/show_all_fights.html"
    context_object_name = "fights"

    def get_queryset(self):
        """Filtering logic for search_fights.html, returns set of Fights that pass the filters"""

        queryset = Fight.objects.all()

        weight_class = self.request.GET.get("weight_class")
        finish = self.request.GET.get("finish")
        min_rating = self.request.GET.get("min_rating")

        if weight_class:
            queryset = queryset.filter(weight_class__weight_class=weight_class)

        if finish:
            queryset = queryset.filter(finish=finish)

        if min_rating:
            #Have to call get_star_rating() method in Fight model on every Fight, so filter by individal ids
            greater_than_fights = [f.id for f in queryset if f.get_star_rating() >= float(min_rating)]
            queryset = queryset.filter(id__in=greater_than_fights)

        return queryset

    def get_context_data(self, **kwargs):
        #Fight fields to filter by in search_fights.html

        context = super().get_context_data(**kwargs)
        context['weight_classes'] = WeightClass.objects.all()
        context['finishes'] = ["DECIS", "UNDEC", "KOTKO", "SUBMI"]
        context['ratings'] = [1, 2, 3, 4, 5]

        return context


class ShowFightView(DetailView):
    """View class to show a single Fight. Inherits from DetailView"""
    
    model = Fight
    template_name = "project/show_fight.html"
    context_object_name = "fight"

class CreateFighterView(CreateView, LoginRequiredMixin):
    """View class to create a new Fighter. Inherits from CreateView"""

    model = Fighter
    template_name = "project/add_fighter_form.html"
    form_class = CreateFighterForm

    def get_success_url(self):
        "Redirects to newly created Fighter page"

        return reverse_lazy("show_fighter", kwargs={"pk": self.object.pk})

class UpdateFighterView(UpdateView, LoginRequiredMixin):
    """View class to update an existing Fighter. Inherits from UpdateView"""

    model = Fighter
    template_name = "project/update_fighter_form.html"
    form_class = UpdateFighterForm

    def get_success_url(self):
        "Redirects to newly updated Fighter page"

        return reverse_lazy("show_fighter", kwargs={"pk": self.object.pk})

class CreateFightView(CreateView, LoginRequiredMixin):
    """View class to create a new Fight. Inherits from CreateView"""

    model = Fight
    template_name = "project/add_fight_form.html"
    form_class = CreateFightForm

    def get_success_url(self):
        "Redirects to newly created Fight page"

        return reverse_lazy("show_fight", kwargs={"pk": self.object.pk})
    
class DeleteFightView(LoginRequiredMixin, DeleteView):
    """View class to delete an existing Fight. Inherits from DeleteView"""

    model = Fight
    template_name = "project/delete_fight_form.html"

    def get_success_url(self):
        "Redirects to Fighter page of the winner of the newly deleted Fight"
        winner = self.object.winner  # Access before deleting
        return reverse_lazy("show_fighter", kwargs={"pk": winner.pk})


class RateFightView(LoginRequiredMixin, CreateView):
    """View class to create a Rating on an existing Fight. Inherits from CreateView"""

    model = Rating
    form_class = RateFightForm
    template_name = "project/rate_fight_form.html"

    def form_valid(self, form):
        "Handles form data, delegate work to super"

        fight = Fight.objects.get(pk=self.kwargs['pk'])
        form.instance.fight = fight
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        "Provides Fight for which Rating is given"

        context = super().get_context_data(**kwargs)
        context["fight"] = Fight.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self):
        "Redirect to Fight which Rating has just rated"

        return reverse_lazy("show_fight", kwargs={"pk": self.kwargs["pk"]})