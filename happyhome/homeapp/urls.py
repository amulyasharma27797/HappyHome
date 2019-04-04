from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.NewUserRegistration.as_view(), name='new_user_registration'),
]
