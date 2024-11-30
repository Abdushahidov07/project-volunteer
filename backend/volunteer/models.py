from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass 


class UserLocation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    latitude = models.FloatField() 
    longitude = models.FloatField()  
    timestamp = models.DateTimeField(auto_now_add=True) 
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f'{self.user.username} - {self.latitude}, {self.longitude}'
    
class Volunteer(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Marker(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"Marker by {self.volunteer.name}"
