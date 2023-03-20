import random
import pyotp
from django.contrib.auth.models import User
from django.db import models
from account.models import userdetails


class phonenumbermodel(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=14)
    key = models.CharField(max_length=50, unique=True, blank=True)
    verifiednumber = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        # Here we are using Time Based OTP. The interval is 60 seconds.
        # otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(str(self.key), interval=300)
        return t.verify(str(provided_otp))
