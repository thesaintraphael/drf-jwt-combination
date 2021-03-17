from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


# class LoginForm(forms.Form):
#     email = forms.EmailField(label="Email")
#     password = forms.CharField(label="Email", widget=forms.PasswordInput)
