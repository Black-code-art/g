from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.contrib.auth.models import User
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    
    Role = {
        ('admin', 'admin'),
        ('user', 'user'),
        ('driver', 'driver'),
    }
    
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name   = models.CharField(max_length=255)
    last_name    = models.CharField(max_length=255)
    image        = models.ImageField(upload_to='images/', null=True)
    email        = models.EmailField(unique=True)
    password     = models.CharField(max_length=255)
    role         = models.CharField(max_length=255, choices=Role)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted   = models.BooleanField(default=False)
    date_joined  = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def _str_(self):
        return f"{self.email} -- {self.id}"
    




class Shipment(models.Model):


    STATUS_CHOICES =(

        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),

    )

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_id =models.CharField(max_length=50, unique=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='customer')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='driver')
    sender_address = models.TextField()
    receiver_address = models.TextField()
    weight = models.FloatField()
    dimensions = models.CharField(max_length=100)  
    # service_level = models.Field(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES ,default='Pending')
    current_location = models.CharField(max_length= 450)
    estimated_delivery_date = models.DateField()
    shipment_history =models.TextField()


    @property
    def customer_data(self):

        return {
            "first_name": self.customer.first_name,
            "last_name": self.customer.last_name,
            "email": self.customer.email,
            "role": self.customer.role
        }
    
    @property
    def driver_data(self):

        return {
            "first_name": self.driver.first_name,
            "last_name": self.driver.last_name,
            "email": self.driver.email,
            "role": self.driver.role
        }







