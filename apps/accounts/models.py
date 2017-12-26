from django.db import models
from django.contrib.models import User
# Create your models here.
class UserProfileInfo(models.Model):

    user = models.OneToOneField(User)
    
