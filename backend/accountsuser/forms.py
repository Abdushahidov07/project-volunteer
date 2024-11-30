from django import forms
from django.contrib.auth.forms import UserCreationForm
from volunteer.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    wallet_balance = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.00, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
