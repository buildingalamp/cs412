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
    # profile_image_url = models.URLField(blank=True) #url as a string
    profile_image_file = models.ImageField(blank=True)

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
    
    def get_images(self):
        """Returns all images related to this StatusMessage"""

        #use reverse foreign key manager to get list of StatusImage related to this StatusMessage
        status_image_list = list(self.statusimage_set.all())
        image_list = [None] * len(status_image_list)

        #iterate over each list of StatusImage
        for n in range(len(status_image_list)):

            #get Image related to StatusImage and insert into list
            image_list[n] = status_image_list[n].image

        return image_list
    
class Image(models.Model):
    """Profile image model"""

    #attributes of Image
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

class StatusImage(models.Model):
    """Images to StatusMessage model"""

    #attributes of StatusImage
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
