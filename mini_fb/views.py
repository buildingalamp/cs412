# File: views.spy
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: views file used to define the view classes

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm

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

class CreateStatusMessageView(CreateView):
    """View class to handle the creation of a new Status Message, inherits from CreateView"""

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self):
        """This method returns the dictionary of context variables for use in the template"""

        #calling the superclass method
        context = super().get_context_data()

        #find/add the profile to the context data
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        #add this profile into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new object
        to the Django database. Adds the foreign key of the Profile to the 
        StatusMessage object before saving it to the database"""

        #instrument our code to display form fields:
        print(f"CreateStatusMessageView.form_valid:form.cleaned_data={form.cleaned_data}")

        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
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

        pk = self.kwargs['pk']

        return reverse('show_profile', kwargs={'pk':pk})
    
class UpdateProfileView(UpdateView):
    """View class to handle the update of Profile"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def form_valid(self, form):
        return super().form_valid(form)