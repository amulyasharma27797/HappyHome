from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserDetails(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    email_id = models.EmailField(max_length=50, unique=True)
    phone = models.IntegerField()
    is_seller = models.BooleanField(default=False)
    description = models.TextField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='media/images/', default='media/images/profile-default-lrg.png')


# class Property(models.Model):
#     title = models.CharField(max_length=50)
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=20)
#     state = models.CharField(max_length=20)
#     pin = models.IntegerField()
#     price = models.IntegerField()
#     bedroom = models.IntegerField()
#     bathroom = models.IntegerField()
#     sq_feet = models.IntegerField()
#     lot_size = models.IntegerField()
#     garage = models.IntegerField()
#     listing_date = models.DateField(auto_now_add=True)
#     description = models.TextField(max_length=200)
#     main_image = models.ImageField(upload_to='media/images/')
#     other_images = models.ImageField(upload_to='media/images/')
