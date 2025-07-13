from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore

# Create your models here.
class User(AbstractUser):
    phone = models.IntegerField(null=True,blank=True,unique=True)
    is_theatre_manager = models.BooleanField(default=False,blank=True,null=True)
    is_approved = models.BooleanField(default=False,)
    otp = models.IntegerField(null=True, blank=True)
    otp_verified = models.BooleanField(default=False,)
    otp_expried=models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self):
        return self.username    