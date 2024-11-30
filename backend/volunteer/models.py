from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    CHOICE_GENDER=(
        ("женщина", "Женщина"),
        ("мужчина", "Мужчина"),
    )
    CHOICE_STATUS=(
        ("валантер", "Валантер"),
        ("Нуждающийся", "Нуждающийся"),
    )
    image = models.ImageField(upload_to="static/images", null=True, blank=True)
    age = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=13,null=True)
    gender = models.CharField(max_length=50, choices=CHOICE_GENDER,null=True)
    status = models.CharField(max_length=50, choices=CHOICE_STATUS,null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

class Category(models.Model):
    category_name = models.CharField(max_length=150)


class ApplyHelp(models.Model):
    CHOICE_STATUSHELP=(
        ("активно", "Активно"),
        ("завершино", "Завершино"),
        ("впроцессе", "Впроцессе"),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="static/images", null=True, blank=True)
    add_time = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    status = models.CharField(max_length=50, choices=CHOICE_STATUSHELP)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}->{self.category.category_name}"
    



class Application(models.Model):
    CHOICE_STATUSHELP=(
        ("активно", "Активно"),
        ("завершино", "Завершино"),
        ("впроцессе", "Впроцессе"),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    applay= models.ForeignKey(ApplyHelp, on_delete=models.CASCADE) 
    description = models.TextField()
    add_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=CHOICE_STATUSHELP)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}->{self.applay.__str__}"
    

class CharityCompany(models.Model):
    company_name = models.CharField(max_length=150)
    location = models.CharField(max_length=250)
    descriptions = models.TextField()
    def __str__(self):
        return self.company_name
          

class ApplicationCharity(models.Model):
    CHOICE_STATUSHELP=(
        ("активно", "Активно"),
        ("завершино", "Завершино"),
        ("впроцессе", "Впроцессе"),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company_charity= models.ForeignKey(CharityCompany, on_delete=models.CASCADE) 
    description = models.TextField()
    add_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=CHOICE_STATUSHELP)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}->{self.company_charity.__str__}"
    


class UserLocation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    latitude = models.FloatField() 
    longitude = models.FloatField()  
    timestamp = models.DateTimeField(auto_now_add=True) 
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f'{self.user.username} - {self.latitude}, {self.longitude}'
    
    
class Marker(models.Model):
    volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f"Marker by {self.volunteer.username}"
