from django.contrib.auth.forms import UserCreationForm

from django import forms

from .models import UserDetails


class RegistrationForm(UserCreationForm):
    email_id = forms.EmailField(max_length=50, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    is_seller = forms.CheckboxInput()

    class Meta:
        model = UserDetails
        fields = ['username', 'first_name', 'last_name', 'email_id',
                  'phone', 'password1', 'password2', 'is_seller',
                  'description', 'photo']


class Login(UserCreationForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'password1']