from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your email address'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter your phone number', 'pattern': '[0-9]{10}'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your username'}),
            
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))

    class Meta:
        model = User
        fields = ('username', 'password')
        
class IdentifyUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    
    
