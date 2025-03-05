from django.db import models
import random
import string
from django.utils import timezone
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from .managers import UserManager  # ✅ Import fixed UserManager
# Create your models here.


class BaseModal(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True
# ankit start
class Service(models.Model):
    service_id = models.AutoField(primary_key=True)  
    image = models.FileField(upload_to='service_images/', max_length=250)  
    service_name = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    status= models.BooleanField(default=False)
    

    def __str__(self):
        return self.service_name  
# ankit end
# richa start


class User(AbstractBaseUser):
    service_id = models.ManyToManyField(Service,null=True,blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_no = models.BigIntegerField(unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=settings.USER_ROLES)
    referral_code = models.CharField(blank=True, null=True, max_length=8)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    unique_code = models.IntegerField(unique=True, blank=True, null=True)  # Removed max_length
    password = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    range_field = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    today_status=models.BooleanField(default=True)
    objects = UserManager()  # ✅ Use fixed UserManager

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'user_type']

    def _str_(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.unique_code:  # Generate only if unique_code is not set
            self.unique_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        while True:
            code = random.randint(10000000, 99999999)  # Generate 8-digit integer
            if not User.objects.filter(unique_code=code).exists():  # Ensure uniqueness
                return code
# richa end


# start 
class BookingSlot(models.Model):
    STATUS_CHOICES = (
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    )
    booking_id = models.AutoField(max_length=6,unique=True,primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    booking_summary = models.TextField(blank=True)
    service_id = models.ManyToManyField(Service,null=True,blank=True)
    is_booked = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

class ConfirmBooking(models.Model):
   service_provider_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_provider')
   booking_id = models.ForeignKey(BookingSlot, on_delete=models.CASCADE)
   user_id = models.ForeignKey(User, on_delete=models.CASCADE)
   amount = models.DecimalField(null=True, decimal_places=2, max_digits=10)
   service_id = models.ManyToManyField(Service,null=True,blank=True)
   is_view = models.BooleanField(default=False)


def save(self, *args, **kwargs):
        if self.booking_id.is_booked:
            raise ValueError("Booking is already confirmed!")
        super().save(*args, **kwargs)
   
# end
    