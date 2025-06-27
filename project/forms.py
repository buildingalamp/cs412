# File: forms.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/25/2025
# Description: forms file used to define forms used for create/update/delete operations

from django import forms
from .models import *

class CreateFighterForm(forms.ModelForm):
    """A form to add a Fighter to the database"""

    class Meta:
        """Associates this form with a model from the database"""
        model = Fighter
        fields = ['name', 'nickname', 'height', 'reach', 'weight_class', 'age',
                  'nationality', 'wins', 'losses', 'draws', 'profile_image', 'fight_image']

class CreateFightForm(forms.ModelForm):
    """A form to add a Fight on a Fighter to the database"""

    class Meta:
        """Associates this form with the Fight model; selects fields"""
        model = Fight
        fields = ['draw', 'winner', 'loser', 'weight_class', 
                  'rounds', 'finish', 'date']

class UpdateFighterForm(forms.ModelForm):
    """A form to update an existing Fighter"""

    class Meta:
        """Associates this form with the Fihter model; selects fields"""
        model = Fighter
        fields = ['name', 'nickname', 'height', 'reach', 'weight_class', 'age',
                  'nationality', 'wins', 'losses', 'draws', 'profile_image', 'fight_image']

class RateFightForm(forms.ModelForm):
    """A form to add a Rating to a Fight to the database"""

    class Meta:
        """Associates this form with the Rating model; selects fields"""
        model = Rating
        fields = ['star_rating']