from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Ride(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    des = models.CharField(max_length=200, verbose_name='Destination')
    start_date = models.DateTimeField(verbose_name='Start Date', help_text='Format: 2019-01-01 12:00')
    arrive_date = models.DateTimeField(verbose_name='Arrive Date', help_text='Format: 2019-01-01 12:00')
    pas_num = models.IntegerField(verbose_name='Passenger Number')
    share_valid = models.BooleanField(default=False, verbose_name='Do you want to share the ride with others?')
    share_max_num = models.IntegerField(verbose_name='The maximum sharers you can accept')
    share_name = models.CharField(max_length=200)
    share_number = models.IntegerField(default=0, verbose_name='Sharer Number')
    driver_name = models.CharField(max_length=200)
    status = models.IntegerField(default=0, verbose_name='Ride Status (open, confirmed, complete)')
    vehicle_type = models.CharField(max_length=200, verbose_name='Vehicle Type', blank=True)
    license_plate_number = models.CharField(max_length=20, verbose_name="License Plate Number", blank=True)
    max_pas_num = models.IntegerField(verbose_name="Maxmium Number of Passengers", default=0)
    # status: 0(open), 1(confirmed), 2(complete)

    def get_absolute_url(self):
        return reverse('ride:owner-view')

class Share(models.Model):

    sharer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    des = models.CharField(max_length=200, verbose_name='Destination')
    start_date_0 = models.DateTimeField(verbose_name='Earliest acceptable start date', help_text='Format: 2019-01-01 12:00')
    start_date_1 = models.DateTimeField(verbose_name='Latest acceptable start date', help_text='Format: 2019-01-01 12:00')
    arrive_date_0 = models.DateTimeField(verbose_name='Earliest acceptable arrive date', help_text='Format: 2019-01-01 12:00')
    arrive_date_1 = models.DateTimeField(verbose_name='Latest acceptable arrive date', help_text='Format: 2019-01-01 12:00')
    pas_num = models.IntegerField(default=1)

    def get_absolute_url(self):
        #return reverse('ride:ride-detail', kwargs={'pk': self.pk})
        return reverse('ride:share-list')
