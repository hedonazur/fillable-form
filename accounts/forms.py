from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Email'), widget=forms.EmailInput(attrs={'placeholder' :_('Email'), 'style': 'width: 300px;'}))
    username = forms.CharField(required=True, label=_('Username'), widget=forms.TextInput(attrs={'placeholder': _('Username'), 'style': 'width: 300px;'}))
    password1 =  forms.CharField(required=True, label=_('Enter password'), widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'style': 'width: 300px;'}))
    password2 = forms.CharField(required=True, label=_('Confirm password'), widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password'), 'style': 'width: 300px;'}))
    
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
        label=_('Old password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Old password'),
                   'style': 'width: 300px;'}))
    new_password1 =  forms.CharField(
        required=True,
        label=_('Enter password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('New password'),
                   'style': 'width: 300px;'}))
    new_password2 = forms.CharField(
        required=True,
        label=_('Confirm password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Confirm new password'),
                   'style': 'width: 300px;'}))


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
                            widget=forms.TextInput(attrs={'id': 'floatingInput', 'class': 'form-control mb-3'}),
                            required=True)
    password = forms.CharField(
                            widget=forms.PasswordInput(attrs={'id': 'floatingPassword', 'class': 'form-control mb-3'}),
                            required=True)

    class Meta:
        model=User
        fields=['username','password']