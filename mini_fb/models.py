# File: models.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: model file used to define database models and their attributes

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    """User profile model"""

    # attributes of Profile
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email_address = models.EmailField(blank=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        """Returns Profile's first and last name as one string"""
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        """Returns the URL to display one instance of Profile"""
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_all_status_messages(self):
        """Returns all StatusMesages of this Profile"""
        messages = StatusMessage.objects.filter(profile=self)
        return messages

class StatusMessage(models.Model):
    """Status message model"""

    # attributes of StatusMessage
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        """Returns StatusMessage's message as string"""
        return f'{self.message}'