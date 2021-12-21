from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Room


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ChangingPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'old-pwd-change','type':'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'new-pwd1-change','type':'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'new-pwd2-change','type':'password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']