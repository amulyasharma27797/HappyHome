import smtplib

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import FormView
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from .forms import RegistrationForm
from .forms import UpdateUser
from .forms import PropertyForm

from .models import UserDetails
from .models import Property
from .models import Enquiry


# Create your views here.


def home(request):
    """Home Page"""
    if request.user.is_authenticated:
        user = UserDetails.objects.get(user=request.user)
        list_latest_property = Property.objects.filter().order_by('-property_listing_date')[:3]
        title = Property.objects.filter().order_by('-title')
        return render(request, 'home.html', {'properties': list_latest_property, 'user': user, 'title': title})
    else:
        list_latest_property = Property.objects.filter().order_by('-property_listing_date')[:3]
        title = Property.objects.filter().order_by('-title')
        return render(request, 'home.html', {'properties': list_latest_property, 'title': title})


# Registering a new user
class NewUserRegistration(FormView):
    form_class = RegistrationForm
    template_name = 'registration_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('login')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'error': form.errors})


@login_required
def register_property(request):
    """Registering a new Property"""
    user = UserDetails.objects.get(user=request.user)
    if request.method == "POST" and user.is_seller:
        property_form = PropertyForm(request.POST, request.FILES)
        if property_form.is_valid():
            property_form.instance.user = user
            property_form.instance.posted_by_id = user.id
            property_form.instance.save()
            return redirect('property_view')
    else:
        property_form = PropertyForm()
        if not user.is_seller:
            return HttpResponse("<h1>You need to be seller to access this page</h1>")

    context = {'form': property_form, 'errors': property_form.errors, 'user': user}
    return render(request, 'property_form.html', context)


@login_required
def property_view(request):
    """View Property for Logged In User"""
    user = UserDetails.objects.get(user=request.user)
    if request.method == "GET" and user.is_seller:
        try:
            property = Property.objects.filter(posted_by=request.user)
            return render(request, 'property_view.html', {'property': property, 'user': user})

        except Property.DoesNotExist:
            return HttpResponse("<h1>The current seller does not have any property</h1>")

    else:
        if not request.user.is_seller:
            return HttpResponse("<h1>You need to be seller to access this page</h1>")
    return render(request, 'property_view.html', {'property': property, 'user': user})


# View Properties for all users
class ListAllProperties(ListView):
    # model = Property
    queryset = Property.objects.order_by('-id')
    template_name = 'Properties.html'
    context_object_name = 'properties'
    paginate_by = 3


# Showing Properties Details
class ShowPropertyDetails(DetailView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super(ShowPropertyDetails, self).get_context_data(**kwargs)
        if str(self.request.user) == 'AnonymousUser':
            context['is_not_anonymous'] = False
        else:
            context['is_not_anonymous'] = True
            context['user'] = UserDetails.objects.get(user=self.request.user)
            context['enquiries'] = Enquiry.objects.filter(property=Property.objects.get(id=self.kwargs['pk']))
        return context


# Update Property
class UpdateProperty(UpdateView):

    model = Property
    fields = ['title', 'address', 'city', 'state', 'pin', 'price',
              'bedroom', 'bathroom', 'sq_feet', 'lot_size', 'garage',
              'description', 'photo1', 'photo2', 'photo3',
              'photo4', 'photo5', 'photo6', ]
    template_name = 'property_update.html'

    def form_valid(self, form):
        form.save()
        return redirect('property_view')


# Delete Property
class DeleteProperty(DeleteView):

    model = Property
    template_name = 'property_delete.html'
    success_url = reverse_lazy('property_view')

    def form_valid(self, form):
        form.save()
        return redirect('property_view')

    def get_context_data(self, **kwargs):
        context = super(DeleteProperty, self).get_context_data(**kwargs)
        context['user'] = UserDetails.objects.get(user=self.request.user)
        return context


def search_property(request):
    """Search Property"""
    if not str(request.user) == 'AnonymousUser':
        user = UserDetails.objects.get(user=request.user)
    else:
        user = ""
    if request.method == "POST":

        query_title = request.POST.get('Title')
        query_city = request.POST.get('City')
        query_state = request.POST.get('State')

        result = Property.objects.filter(title__contains=query_title, city__contains=query_city, state__contains=query_state)
        result.union(Property.objects.filter(title__contains=query_title, city__contains=query_city, state__contains=query_state))
        context = {'properties': result, 'user': user}
        if len(result) == 0:
            context['no_result_found'] = True
        return render(request, 'Properties.html', context)


def make_enquiry(request, pid):
    """Enquiry"""
    try:

        enquiry = Enquiry()
        enquiry.property = Property.objects.get(id=pid)
        enquiry.person = UserDetails.objects.get(username=request.user)
        enquiry.description = request.POST.get('Query')
        EMAIL_ADDRESS = "amulya.sharma@tothenew.com"
        PASSWORD = "************"
        # seller_email = UserDetails.objects.get(id=pid).email_id
        # enquiry.save()
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(enquiry.property.title, enquiry.description)
        server.sendmail(EMAIL_ADDRESS, 'amulysharma27797@gmail.com', message)
        server.quit()
        return redirect('list_all_properties')

    except:
        return HttpResponse("Email failed to send")


# List All Enquiries Made
@login_required
def list_enquiries(request):
    user = UserDetails.objects.get(user=request.user)
    if request.method == "GET":
        try:
            enquiry = Enquiry.objects.filter(person=request.user)
            return render(request, 'enquiries.html', {'enquiries': enquiry, 'user': user})

        except Enquiry.DoesNotExist:
            return HttpResponse("<h1>The current seller does not have any property</h1>")


@login_required
def user_detail(request):
    """User Details"""
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

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        if str(self.request.user) == 'AnonymousUser':
            context['is_not_anonymous'] = False
        else:
            context['is_not_anonymous'] = True
            context['user'] = UserDetails.objects.get(user=self.request.user)
        return context


# Contact HTML
class Contact(TemplateView):
    template_name = 'Contact.html'

    def get_context_data(self, **kwargs):
        context = super(Contact, self).get_context_data(**kwargs)
        if str(self.request.user) == 'AnonymousUser':
            context['is_not_anonymous'] = False
        else:
            context['is_not_anonymous'] = True
            context['user'] = UserDetails.objects.get(user=self.request.user)
        return context







