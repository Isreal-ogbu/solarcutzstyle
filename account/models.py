from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class userdetails(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    userprofilepicture = models.ImageField(upload_to="profile/")
