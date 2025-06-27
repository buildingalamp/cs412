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
    
    def get_fighters(self):
        """Returns all fighters of this instance of WeightClass"""

        fighters = Fighter.objects.filter(weight_class=self)
        return fighters

class Fighter(models.Model):
    """Fighter model"""
    
    #attributes of Fighter
    profile_image = models.ImageField(blank=True)
    fight_image = models.ImageField(blank=True)
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
    
    def get_fights(self):
        """Returns all Fights of this Fighter"""

        fight_list = []
        #find Fights where Fighter either won or lost
        for f in Fight.objects.filter(winner=self):
            fight_list.append(f)
        for f in Fight.objects.filter(loser=self):
            fight_list.append(f)     

        return list(fight_list)


class Finish(models.TextChoices):
    """Finish choices, choice of: “Decision”, “Unanimous decision”, “KO/TKO”, “Submission”"""

    DECISION = "DECIS", "Decision"
    UNANIMOUSDECISION = "UNDEC", "Unanimous decision"
    KOTKO = "KOTKO", "KO/TKO"
    SUBMISSION = "SUBMI", "Submission"

class Fight(models.Model):
    """Fight model"""

    #attributes of Fight
    draw = models.BooleanField(blank=True) #true = fight was drawn, false = fight had a winner
    winner = models.ForeignKey("Fighter", related_name="winner", on_delete=models.CASCADE)
    loser = models.ForeignKey("Fighter", related_name="loser", on_delete=models.CASCADE)
    weight_class = models.ForeignKey("WeightClass", on_delete=models.CASCADE)
    rounds = models.IntegerField(blank=True)
    finish = models.CharField(max_length=5, choices=Finish, default=Finish.DECISION)
    date = models.DateField(blank=True)

    def __str__(self):
        """Returns Fight's two Fighters as a string"""

        return f'{self.winner.name} vs {self.loser.name}'
    
    def get_star_rating(self):
        """Returns the average of all Ratings of a Fight"""

        #fet all ratings
        ratings = list(Rating.objects.filter(fight=self))
        average_star_rating = 0

        if ratings:
            #iterate over ratings
            for i in range(len(ratings)):
                #add
                average_star_rating += ratings[i].star_rating
            #average
            average_star_rating = average_star_rating/len(ratings)
            
        #returns 0 if there are no ratings, minimum rating score is 1
        return average_star_rating

class Rating(models.Model):
    """Fight rating model"""

    #attributes of Rating
    fight = models.ForeignKey("Fight", on_delete=models.CASCADE)
    star_rating = models.IntegerField(blank=True) #choice of 1-5

    def __str__(self):
        """Returns the Fight that Rating is rating as a string"""

        return f'{self.fight}'