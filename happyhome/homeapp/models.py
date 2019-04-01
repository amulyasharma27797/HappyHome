from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    image = models.ImageField(blank=True)
    user_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.IntegerField()