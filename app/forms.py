from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'})
                   }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current_password',
                                                                 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput
    (attrs={'autocomplete': 'current_password', 'class': 'form-control', 'autofocus': True}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput
    (attrs={'autocomplete': 'new-password', 'class': 'form-control', 'autofocus': True}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput
    (attrs={'autocomplete': 'new-password', 'class': 'form-control', 'autofocus': True}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput
    (attrs={'autocomplete': 'email', 'class': 'form-control', 'autofocus': True}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput
    (attrs={'autocomplete': 'new-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput
    (attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        labels = {'name': 'Name', 'locality': 'Locality', 'city': 'City', 'state': 'State', 'zipcode': 'Zipcode'}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'locality': forms.TextInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   'state': forms.Select(attrs={'class': 'form-control'}),
                   'zipcode': forms.NumberInput(attrs={'class': 'form-control'})
                   }
