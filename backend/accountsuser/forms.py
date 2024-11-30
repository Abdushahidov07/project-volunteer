from django import forms
from django.contrib.auth.forms import UserCreationForm
from volunteer.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','password1', 'password2']

        # fields = ['username','first_name','last_name','age','phone_number','gender','status','password1', 'password2']
