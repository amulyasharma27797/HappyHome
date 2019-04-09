from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('show/', views.show, name='show'),
    path('home/', views.home, name='home'),
    path('registration/', views.NewUserRegistration.as_view(), name='new_user_registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('property_register/', views.PropertyRegistration.as_view(), name='property_register'),
    path('property/', views.ShowProperty.as_view(), name='property'),
    path('user/', views.user_detail, name='user'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
]


# superuser
# username = ttn
# password = ttn
# email = ttn@ttn.com
