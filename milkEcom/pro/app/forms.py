from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from app.models import Customer


class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'auto-focus':'True','class':'form-control'}))
    password=UsernameField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields= ['name','locality','city','mobile','state','zipcode']

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }

class MyPasswordChange(PasswordChangeForm):
    old_password=forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password','autofocus':'True'}))
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplte':'current-password','autofocus':'True'}))
    new_password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','autofocus':'True','autocomplete':'current-password'}))


class PasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    
class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password'}))
    new_password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':'current-password'}))