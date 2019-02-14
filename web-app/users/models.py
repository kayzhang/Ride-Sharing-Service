from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isDriver = models.BooleanField(default=False, verbose_name='Do you want to register as a driver?')
    vehicle_type = models.CharField(max_length=200, verbose_name='Vehicle Type')
    license_plate_number = models.CharField(max_length=20, verbose_name="License Plate Number", blank=True)
    max_pas_num = models.IntegerField(verbose_name="Maxmium Number of Passengers", default=0)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
