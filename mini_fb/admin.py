# File: admin.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/5/2025
# Description: used to create an admin profile, giving us
# admin privileges in order to create and edit profiles

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage, Friend
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)