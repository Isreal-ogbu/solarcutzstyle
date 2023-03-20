from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class servicemodel(models.Model):
    service_picture = models.ImageField(upload_to="service/")
    service_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class stylemodel(models.Model):
    service_picture = models.ForeignKey(servicemodel, on_delete=models.CASCADE)
    style_picture = models.ImageField(upload_to="style/", null=False)
    style_description = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class offermodel(models.Model):
    offer_picture = models.ImageField(upload_to='offer/', null=False)
    offer_discription_top = models.CharField(max_length=20)
    offer_discription_button = models.CharField(max_length=40)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class stylistmodel(models.Model):
    sylist_picture = models.ImageField(upload_to="stylist/")
    stylist = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stylist


class bookmodels(models.Model):
    options = [
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor")
    ]
    user_detail = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(servicemodel, on_delete=models.CASCADE)
    style = models.ForeignKey(stylemodel, on_delete=models.CASCADE)
    stylist = models.ForeignKey(stylistmodel, on_delete=models.CASCADE)
    option = models.CharField(choices=options, max_length=100)
    service_Time = models.DateTimeField()
    amount = models.CharField(max_length=99999999)
    additional_info = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
