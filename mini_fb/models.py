# File: models.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: model file used to define database models and their attributes

from django.db import models
from django.db. models import Q
from django.urls import reverse
import sys

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
    
    #StatusMessage methods
    def get_all_status_messages(self):
        """Returns all StatusMesages of this Profile"""
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    #Friend methods
    def get_friends(self):
        """Returns all Friend relation of this Profile"""

        #find Friends where Profile is either profile1 or profile2
        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)

        #seperate the other Profile and put into list
        friend_list = []
        for f in friends1:
            friend_list.append(f.profile2)
        for f in friends2:
            friend_list.append(f.profile1)

        return friend_list
    
    def add_friend(self, other):
        """Creates new Friend relation between this Profile and other Profile"""

        #check for self-friending
        if self==other:
            return
        
        #check for duplicates
        if (Friend.objects.filter(profile1=self, profile2=other) or
            Friend.objects.filter(profile2=self, profile1=other)).exists():
            return
        
        #create Friend
        new_friend = Friend(profile1=self, profile2=other)
        new_friend.save()

    def get_friend_suggestions(self):
        """"Returns all Profiles not currently Friends with this Profile"""

        friend_suggestions_list = []

        #list of non-candidates: current friends and this profile
        current_friends = self.get_friends()
        
        #get pks for comparison
        current_friends_pk = []
        for friend in current_friends:
            current_friends_pk.append(friend.pk)

        #add all profiles not in current_friends
        for friend in Profile.objects.all():
            if friend.pk not in current_friends_pk and friend.pk != self.pk:
                friend_suggestions_list.append(friend)

        return list(friend_suggestions_list)

        # current_friends = self.get_friends()
        # return Profile.objects.exclude(Q(id=self.id) | Q(id__in=[p.id for p in current_friends]))

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
    profile = models.ForeignKey("Profile", blank=True, null=True, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

class StatusImage(models.Model):
    """Images to StatusMessage model"""

    #attributes of StatusImage
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

class Friend(models.Model):
    """"Friend model, associates two Profile"""

    #attributes of Friend
    profile1 = models.ForeignKey("Profile", related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey("Profile", related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Returns the two related Profile as string"""
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'