from django import forms
from django_countries.fields import CountryField

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    verify_password = forms.CharField(widget=forms.PasswordInput, label='Verify Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        verify_password = cleaned_data.get('verify_password')

        if password and verify_password and password != verify_password:
            raise forms.ValidationError("Passwords do not match. Please try again.")

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)