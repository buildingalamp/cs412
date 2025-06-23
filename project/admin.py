# File: admin.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/20/2025
# Description: used to create an admin profile, giving us
# admin privileges in order to create and edit profiles

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(WeightClass)
admin.site.register(Fighter)
admin.site.register(Image)
admin.site.register(Fight)