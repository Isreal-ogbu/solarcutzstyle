from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class userdetails(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    userprofilepicture = models.ImageField(upload_to="profilePicture/")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
