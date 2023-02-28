from django.urls import path
from rest_framework import routers
from .views import serviceviewset, styleviewset, offerviewset, stylistviewset, bookingsviewset, service_style_view

router = routers.SimpleRouter()

router.register(r"styles", styleviewset, basename='styles')
router.register(r"stylist", stylistviewset, basename='stylist')
router.register(r"services", serviceviewset, basename='services')
router.register(r"offers", offerviewset, basename='offers')
router.register(r"booking", bookingsviewset, basename='booking')

urlpatterns = [
    path("s/<int:pk1>/", service_style_view.as_view(), name='all_service/style'),
    path("s/<int:pk1>/<int:pk2>/", service_style_view.as_view(), name='instance_service/style')
] + router.urls
