# File: models.py
# Author: Jeffrey Zhou (jzhou25@bu.edu), 6/20/2025
# Description: model file used to define database models and their attributes

from django.db import models

# Create your models here.

class WeightClass(models.Model):
    """Weight class models"""

    #attributes of WeightClass
    weight_class = models.TextField(blank=True) #choice of = "Flyweight", "Bantamweight", 
                                                #"Featherweight", "Lightweight", "Welterweight"
                                                #"Middleweight", "Light Heavyweight", "Heavyweight"

    def __str__(self):
        """Returns WeightClass's weight_class as a string"""
        return f'{self.weight_class}'
    

class Fighter(models.Model):
    """Fighter model"""
    
    #attributes of Fighter
    name = models.TextField(blank=True)
    nickname = models.TextField(blank=True)
    height = models.IntegerField(blank=True) #in cm
    reach = models.IntegerField(blank=True) #in cm
    weight_class = models.ForeignKey("WeightClass", on_delete=models.CASCADE)
    age = models.IntegerField(blank=True)
    nationality = models.TextField(blank=True)
    wins = models.IntegerField(blank=True)
    losses = models.IntegerField(blank=True)
    draws = models.IntegerField(blank=True)

    def __str__(self):
        """Returns Fighter's name as a string"""
        return f'{self.name}'

class Image(models.Model):
    """Fighter image model"""

    #attributes of Image
    fighter = models.ForeignKey("Fighter", blank=True, null=True, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        """Returns Images's fighter name as a string"""
        return f'{self.fighter.name}'

class Fight(models.Model):
    """Fight model"""

    #attributes of Fight
    fight_card = models.TextField(blank=True)
    draw = models.BooleanField(blank=True) #true = fight was drawn, false = fight had a winner
    winner = models.ForeignKey("Fighter", related_name="winner", on_delete=models.CASCADE)
    loser = models.ForeignKey("Fighter", related_name="loser", on_delete=models.CASCADE)
    weight_class = models.ForeignKey("WeightClass", on_delete=models.CASCADE)
    rounds = models.IntegerField(blank=True)
    finish = models.TextField(blank=True) #choice of: “Decision”, “Unanimous decision”, “KO/TKO”, “Submission”
    date = models.DateField(blank=True)

    def __str__(self):
        """Returns Fight's two Fighters as a string"""
        return f'{self.winner.name} vs {self.loser.name}'