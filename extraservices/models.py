from django.contrib.auth.models import User
from django.db import models
import datetime


# Create your models here.

class contact_supportmodel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_problem = models.TextField(max_length=300, null=False)
    date_added = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f"{self.owner} : {self.contact_problem}"


class idea_suggestionmodel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    idea_suggestion = models.TextField(max_length=300, null=False)
    date_added = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f"{self.owner} : {self.idea_suggestion}"
