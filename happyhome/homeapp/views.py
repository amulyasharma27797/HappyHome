# from django.contrib.auth import authenticate, login
import pdb

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, TemplateView, ListView, DetailView, UpdateView

from .forms import RegistrationForm, UpdateUser
from .forms import PropertyForm

from .models import UserDetails, Property
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
@login_required
def register_property(request):
    user = UserDetails.objects.get(user=request.user)
    if request.method == "POST" and user.is_seller:
        property_form = PropertyForm(request.POST, request.FILES)
        if property_form.is_valid():
            property_form.instance.user = user
            property_form.instance.posted_by_id = user.id
            property_form.instance.save()
            return redirect('property')
    else:
        property_form = PropertyForm()
        if not user.is_seller:
            return HttpResponse("<h1>You need to be seller to access this page</h1>")

    context = {'form': property_form, 'errors': property_form.errors}
    return render(request, 'property_form.html', context)


# # View Property for Logged In User
@login_required
def property_view(request):
    user = UserDetails.objects.get(user=request.user)
    if request.method == "GET" and user.is_seller:
        try:
            property = Property.objects.filter(posted_by=request.user)
            return render(request, 'property_view.html', {'property': property})

        except Property.DoesNotExist:
            return HttpResponse("<h1>The current seller does not have any property</h1>")

    else:
        if not request.user.is_seller:
            return HttpResponse("<h1>You need to be seller to access this page</h1>")


# class PropertyView(ListView):
#     model = Property
#     template_name = 'property_view.html'
#     context_object_name = 'property'

# View Properties for all users
class ListAllProperties(ListView):
    model = Property
    template_name = 'Properties.html'
    context_object_name = 'properties'
    paginate_by = 2


# Showing Properties Details
class ShowPropertyDetails(DetailView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'properties'


# Update Property
class UpdateProperty(UpdateView):
    model = Property
    fields = ['title', 'address', 'city', 'state', 'pin', 'price',
              'bedroom', 'bathroom', 'sq_feet', 'lot_size', 'garage',
              'description', 'photo1', 'photo2', 'photo3',
              'photo4', 'photo5', 'photo6', ]
    template_name = 'property_update.html'


# User Details
@login_required
def user_detail(request):

    # return render(request, 'user_profile.html', {'update': user})
    if request.method == "POST":
        user = UserDetails.objects.get(user=request.user)
        update_form = UpdateUser(request.POST, request.FILES, instance=user)
        if update_form.is_valid():
            update_form.save()
            return redirect('user_profile')

    else:
        user = UserDetails.objects.get(user=request.user)
        update_form = UpdateUser(instance=user)

    return render(request, 'user_profile.html', {'update': update_form, 'user': user})










# About HTML
class About(TemplateView):
    template_name = 'About.html'


# Contact HTML
class Contact(TemplateView):
    template_name = 'Contact.html'







