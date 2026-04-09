from django import forms
from django.contrib.auth.models import User
import re


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name", 
        max_length=20, 
        required=True,
        error_messages={'required': 'Please fill in your first name'}
    )
    last_name = forms.CharField(
        label="Last Name", 
        max_length=20, 
        required=True,
        error_messages={'required': 'Please fill in your last name'}
    )
    username = forms.CharField(
        label="Username", 
        max_length=50, 
        required=True,
        error_messages={'required': 'Please fill in your username'}
    )
    email = forms.EmailField(
        label="Email", 
        required=True,
        error_messages={'required': 'Please fill in your email'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Password", 
        required=True,
        error_messages={'required': 'Please fill in your password'}
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        # Only letters, no numbers or special characters
        if not re.fullmatch(r'[A-Za-z]+', first_name):
            raise forms.ValidationError("First name must contain letters only")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.fullmatch(r'[A-Za-z]+', last_name):
            raise forms.ValidationError("Last name must contain letters only")
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise forms.ValidationError("Enter a valid email address")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters")
        if not any(char.isdigit() or not char.isalnum() for char in password):
            raise forms.ValidationError("Password must contain a number or special character")
        return password

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

