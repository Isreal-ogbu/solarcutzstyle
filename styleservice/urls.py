from django.urls import path
from rest_framework import routers
from .views import serviceviewset, styleviewset, offerviewset, stylistviewset, bookingsviewset

router = routers.SimpleRouter()

router.register(r"styles", styleviewset, basename='styles')
router.register(r"stylist", stylistviewset, basename='stylist')
router.register(r"services", serviceviewset, basename='services')
router.register(r"offers", offerviewset, basename='offers')
router.register(r"booking", bookingsviewset, basename='bookin')

urlpatterns = [
] + router.urls
