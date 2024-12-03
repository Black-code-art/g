from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager
from django.contrib.auth.models import User
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    
    Role = {
        ('admin', 'admin'),
        ('user', 'user')
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
    

class Role(models.TextChoices):
    DRIVER = 'DR', 'Driver'
    CUSTOMER = 'CU', 'Customer'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=Role.choices)

class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)

class Job(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='jobs')
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assigned_jobs', null=True, blank=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    pickup_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending') 

class Shipment (models.Model):
    STATUS_CHOICES =[
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),

    ]
        
    


    tracking_id =models.CharField(max_length=50, unique=True)
    sender_address = models.TextField()
    receiver_address = models.TextField()
    weight = models.FloatField()
    dimensions = models.CharField(max_length=100)  
    service_level = models.Field(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES ,default='Pending')
    current_location = models.CharField(max_length= 450)
    estimated_delivery_date = models.DateField()
    shipment_history =models.TextField() 

class Inventory(models.Model):
    warehouse_id = models.CharField(max_length=50)
    item_name = models.CharField (max_length=100) 
    quantity = models.IntegerField()
    restock_level = models.IntegerField 
class Driver(models.Model):
    driver_id =models.CharField(max_length=50, unique= True)
    vehicle_details = models.CharField(max_length=500)

class RouteOptimization(models.Model) :
    delivery_addresses =models.TextField()  
    optimized_route_details = models.TextField()  
