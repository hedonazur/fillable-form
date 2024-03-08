from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'placeholder' :'Email', 'style': 'width: 300px;'}))
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username', 'style': 'width: 300px;'}))
    password1 =  forms.CharField(required=True, label='Enter password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'style': 'width: 300px;'}))
    password2 = forms.CharField(required=True, label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'style': 'width: 300px;'}))
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    

class PasswordChangeForm(PasswordChangeForm):
    old_password =  forms.CharField(
        required=True,
        label='Old password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Old password',
                   'style': 'width: 300px;'}))
    new_password1 =  forms.CharField(
        required=True,
        label='Enter password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'New password',
                   'style': 'width: 300px;'}))
    new_password2 = forms.CharField(
        required=True,
        label='Confirm password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm new password',
                   'style': 'width: 300px;'}))
    