from django.db import models

# Create your models here.
class Profile(models.Model):
    "User profile model"

    # attributes of profile
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email_address = models.EmailField(blank=True)
    profile_img_url = models.URLField(blank=True)

    def __str__(self):
        "return profile's first and last name"
        return f'{self.first_name} {self.last_name}'