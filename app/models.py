from django.db import models
from django.conf import settings
from django.db import models
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator
import binascii
from django.utils import timezone   
import os


# Create your models here.
class UploadImage(models.Model):  
    caption = models.CharField(max_length=200)  
    image = models.ImageField(upload_to='images')  
  
    def __str__(self):  
        return self.caption  

class UserModel(models.Model):
    username = models.CharField(max_length = 100)
    email = models.EmailField(validators = [EmailValidator])
    password = models.CharField(max_length = 250, 
                                validators = [MaxLengthValidator(limit_value = 250), 
                                            MinLengthValidator(limit_value = 8, 
                                                               message = "Password must be at least 8 characters")])
    title = models.CharField(max_length=50)
    image = models.ForeignKey(UploadImage, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)  # Assuming this field stores the Stripe customer ID

    # Additional fields related to the user profile can be added here

    def __str__(self):
        return self.user.username
class CustomToken(models.Model):
    key = models.CharField(max_length=40)
    user = models.OneToOneField(UserModel, related_name='custom_token', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def generate_key(self):
        self.key = binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key
    