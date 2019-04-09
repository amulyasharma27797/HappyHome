# from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, TemplateView, ListView

from .forms import RegistrationForm, UpdateUser
from .forms import PropertyForm

from .models import UserDetails
# Create your views here.


# Home page
def home(request):
    return render(request, 'home.html')


# Registering a new user
class NewUserRegistration(FormView):
    form_class = RegistrationForm
    template_name = 'registration_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('login')

    def form_invalid(self, form):
        return redirect('new_user_registration')


# Registering a new Property
class PropertyRegistration(FormView):
    form_class = PropertyForm
    template_name = 'property_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('property')


# Showing Properties
class ShowProperty(TemplateView):
    template_name = 'Properties.html'


# User Details
@login_required
def user_detail(request):

    # return render(request, 'user.html', {'update': user})
    if request.method == "POST":
        user = UserDetails.objects.get(user=request.user)
        update_form = UpdateUser(request.POST, request.FILES, instance=user)
        if update_form.is_valid():
            update_form.save()
            return redirect('user')

    else:
        user = UserDetails.objects.get(user=request.user)
        update_form = UpdateUser(instance=user)

    return render(request, 'user.html', {'update': update_form, 'user': user})










# About HTML
class About(TemplateView):
    template_name = 'About.html'


# Contact HTML
class Contact(TemplateView):
    template_name = 'Contact.html'







