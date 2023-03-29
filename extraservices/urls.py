from django.urls import path
from rest_framework import routers
from .views import contactviewset, ideagenerationviewset

router = routers.SimpleRouter()

router.register(r"idea", contactviewset, basename='idea')
router.register(r"contact", ideagenerationviewset, basename='contact')


urlpatterns = [
] + router.urls