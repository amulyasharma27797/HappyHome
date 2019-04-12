from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserDetails(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    email_id = models.EmailField(max_length=50, unique=True)
    phone = models.IntegerField()
    is_seller = models.BooleanField(default=False)
    description = models.TextField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='images/', default='images/profile-default-lrg.png')


PROPERTY_CITY_CHOICES = (
        ('panaji', 'Panaji'),
        ('New Delhi', 'New Delhi'),
        ('Faridabad', 'Faridabad'),
        ('Chandigarh', 'Chandigarh'),
    )
PROPERTY_STATE_CHOICES = (
        ('goa', 'Goa'),
        ('delhi', 'Delhi'),
        ('haryana', 'Haryana'),
        ('punjab', 'Punjab'),
    )


class Property(models.Model):
    posted_by = models.ForeignKey(User, related_name='property', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20, choices=PROPERTY_CITY_CHOICES)
    state = models.CharField(max_length=20, choices=PROPERTY_STATE_CHOICES)
    pin = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)
    bedroom = models.IntegerField(blank=False)
    bathroom = models.IntegerField(blank=False)
    sq_feet = models.IntegerField(blank=False)
    lot_size = models.IntegerField(default=0)
    garage = models.IntegerField(default=0)
    property_listing_date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=200, blank=True)
    main_image = models.ImageField(upload_to='images_property/', default='images_property/default_property.jpg')
    photo1 = models.ImageField(upload_to='images_property/', blank=True)
    photo2 = models.ImageField(upload_to='images_property/', blank=True)
    photo3 = models.ImageField(upload_to='images_property/', blank=True)
    photo4 = models.ImageField(upload_to='images_property/', blank=True)
    photo5 = models.ImageField(upload_to='images_property/', blank=True)
    photo6 = models.ImageField(upload_to='images_property/', blank=True)

    def __str__(self):
        return self.title


