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
    def __str__(self):
        return self.category_name 


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
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
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
    
    

class MissingPerson(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=CustomUser.CHOICE_GENDER, null=True)
    description = models.TextField(null=True, blank=True)
    last_known_latitude = models.FloatField()
    last_known_longitude = models.FloatField()
    reported_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  
    reported_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.reported_time}"

class Message(models.Model):
    text = models.TextField()  # Текст сообщения
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Пользователь, который отправил сообщение
    missing_person = models.ForeignKey('MissingPerson', on_delete=models.CASCADE)  # Кому принадлежит пропавший человек
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отправки сообщения

    def __str__(self):
        return f"Сообщение от {self.author.username} - {self.text[:30]}..."

class Marker(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"Marker by {self.user.username}"



class SearchGroup(models.Model):
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    join_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search group for {self.missing_person.name} by {self.user.username}"


class SearchMarker(models.Model):
    search_group = models.ForeignKey(SearchGroup, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Marker by {self.search_group.user.username} for {self.search_group.missing_person.name}"
