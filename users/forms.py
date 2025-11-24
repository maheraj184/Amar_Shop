from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class':'form-control', 'placeholder':'Enter your email'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Enter your username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Enter password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Enter password'
    }))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your address','rows':3}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your phone'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email'}),
        }
