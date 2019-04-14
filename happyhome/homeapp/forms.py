from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.forms import ModelForm

from .models import UserDetails, Enquiry
from .models import Property


# User Registration Form
class RegistrationForm(UserCreationForm):
    email_id = forms.EmailField(max_length=50, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    is_seller = forms.CheckboxInput()

    class Meta:
        model = UserDetails
        fields = ['username', 'first_name', 'last_name', 'email_id',
                  'phone', 'password1', 'password2', 'is_seller',
                  'description', 'photo']


# Property Registration Form
class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'address', 'city', 'state', 'pin', 'price',
                  'bedroom', 'bathroom', 'sq_feet', 'lot_size', 'garage',
                  'description', 'main_image', 'photo1', 'photo2', 'photo3',
                  'photo4', 'photo5', 'photo6']


# User Details Update Form
class UpdateUser(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['username', 'first_name', 'last_name', 'email_id', 'phone', 'description', 'photo']


class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = ['description']
