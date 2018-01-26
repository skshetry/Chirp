from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class User_details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(max_length=300, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        null=True,
    )
    # file = models.ImageField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_details.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_details.save()
