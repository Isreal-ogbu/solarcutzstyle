from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import phonenumbermodel
import pyotp


def is_unique(key):
    try:
        phonenumbermodel.objects.get(key=key)
    except phonenumbermodel.DoesNotExist:
        return True
    return False


def generate_key():
    """User otp key generator"""
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()


@receiver(pre_save, sender=phonenumbermodel)
def create_key(sender, instance, **kwargs):
    """This creates the key for the users that don't have"""
    if not instance.key:
        instance.key = generate_key()
