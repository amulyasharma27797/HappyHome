from django.urls import path
from . import views

urlpatterns = [
    path('func/', views.func, name='try_func'),
]
