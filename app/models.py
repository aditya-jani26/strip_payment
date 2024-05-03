from django.db import models
from django.conf import settings
from django.db import models
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator


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
    
