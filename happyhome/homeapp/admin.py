from django.contrib import admin

from .models import UserDetails
from .models import Property
# Register your models here.


admin.site.register(UserDetails)
admin.site.register(Property)
