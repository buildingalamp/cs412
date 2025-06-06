# File: forms.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: forms file used to define forms used for create/update/delete operations

from django import forms
from .models import Profile, StatusMessage, Image, StatusImage

class CreateProfileForm(forms.ModelForm):
    """A form to add a profile to the database"""

    class Meta:
        """Associates this form with a model from the databse"""
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_file']

class CreateStatusMessageForm(forms.ModelForm):
    """A form to add a status message on a profile to the database"""

    class Meta:
        """Associates this form with the StatusMessage model; selects fields"""
        model = StatusMessage
        fields = ['message']