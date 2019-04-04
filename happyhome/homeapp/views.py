from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import FormView

from .forms import RegistrationForm, Login
# Create your views here.


# Logging in the user
def login(request):
    form = Login
    context_data = {'form': form}
    return render(request, 'login.html', context_data)


# Registering a new user
class NewUserRegistration(FormView):
    form_class = RegistrationForm
    template_name = 'registration_form.html'

    def form_valid(self, form):
        form.save()
        # change to go somewhere else
        return redirect('login')

    def form_invalid(self, form):
        return redirect('new_user_registration')

