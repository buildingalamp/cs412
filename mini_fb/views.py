# File: views.spy
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: views file used to define the view classes

import django.views.generic
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm

# Create your views here.
class ShowAllProfilesView(ListView):
    """View class to show all profiles, inherits from ListView"""

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"


class ShowProfilePageView(DetailView):
    """View class to show a single profile, inherits from DetailView"""

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    """View class to handle the creation of a new Profile, inherits from CreateView"""

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs:any):
        """method to handle user registration form"""
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        """method to handle the submission of the form"""
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()

            login(self.request, user)
            form.instance.user = user

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """View class to handle the creation of a new Status Message, inherits from CreateView"""

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        """return the url for this app's login page"""

        return reverse('login')

    def get_context_data(self):
        """This method returns the dictionary of context variables for use in the template"""

        #calling the superclass method
        context = super().get_context_data()

        # #find/add the profile to the context data
        # #retrieve the PK from the URL pattern
        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)

        user = self.request.user
        profile = Profile.objects.get(user=user)

        #add this profile into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new object
        to the Django database. Adds the foreign key of the Profile to the 
        StatusMessage object before saving it to the database"""

        #instrument our code to display form fields:
        print(f"CreateStatusMessageView.form_valid:form.cleaned_data={form.cleaned_data}")

        #find the logged in user
        user = self.request.user
        profile = Profile.objects.get(user=user)

        # #retrieve the PK from the URL pattern
        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)
        #attach this Profile to the StatusMessage
        form.instance.profile = profile

        #save the status message to the database
        sm = form.save()

        #read the file from the form
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image(image_file=file)
            image.save()

            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()

        #delegate the work to the superclass method form_valid
        return super().form_valid(form)
    
    def get_success_url(self):
        """This method provides a URL to redirect to after creating a new StatusMessage"""

        user = self.request.user
        profile = Profile.objects.get(user=user)

        return redirect('show_profile', profile.pk)
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View class to handle the update of Profile"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        """return the url for this app's login page"""

        return reverse('login')

    def form_valid(self, form):
        return super().form_valid(form)

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """View class to handle the deletion of StatusMessage"""

    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = 'status_message'

    def get_login_url(self):
        """return the url for this app's login page"""

        return reverse('login')

    def get_success_url(self):
        "Returns the URL of the profile"

        #get the pk for this StatusMessage
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)

        #find the Profile to which this StatusMessage is related to by FK
        profile = status_message.profile

        #reverse to show the Profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """View class to handle the updating of StatusMessage"""

    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'status_message'

    def get_login_url(self):
        """return the url for this app's login page"""

        return reverse('login')

    def get_success_url(self):
        "Returns the URL of the profile"

        #get the pk for this StatusMessage
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)

        #find the Profile to which this StatusMessage is related to by FK
        profile = status_message.profile

        #reverse to show the Profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
class AddFriendView(LoginRequiredMixin, django.views.generic.View):
    """View class to handle adding new Friends"""

    model = Profile

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        """return the url for this app's login page"""

        return reverse('login')
        
    def dispatch(self, request, *args, **kwargs):
        """Method to handle the creation of new Friends"""
        #get Profiles pk from url
        other_pk = self.kwargs.get('other_pk')

        #get Profiles from pk
        user = request.user
        profile = Profile.objects.get(user=user)
        other_profile = Profile.objects.get(pk=other_pk)

        #add friend
        profile.add_friend(other_profile)

        #redirect back to profile page
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    """"View class to handle showing friend suggestions"""

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        """return the url for this app's login page"""

        return reverse('login')

    model = Profile
    context_object_name = 'profile'
    template_name = "mini_fb/friend_suggestions.html"

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """"View class to handle showing news feed"""

    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

    def get_login_url(self):
        """return the url for this app's login page"""

        return reverse('login')
    model = Profile
    context_object_name = 'profile'
    template_name = "mini_fb/news_feed.html"