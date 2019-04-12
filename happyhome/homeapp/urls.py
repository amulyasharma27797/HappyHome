from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('show/', views.show, name='show'),
    path('home/', views.home, name='home'),
    path('registration/', views.NewUserRegistration.as_view(), name='new_user_registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('property_register/', views.register_property, name='property_register'),
    path('property_view/', views.property_view, name='property_view'),
    # path('property_view/', views.PropertyView.as_view(), name='property_view'),
    path('property_list/', views.ListAllProperties.as_view(), name='list_all_properties'),
    path('property_details/<int:pk>/', views.ShowPropertyDetails.as_view(), name='property_details'),
    path('property_update/<int:pk>/', views.UpdateProperty.as_view(), name='property_update'),
    path('user/', views.user_detail, name='user_profile'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
]


# superuser
# username = ttn
# password = ttn
# email = ttn@ttn.com
