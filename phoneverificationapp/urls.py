from phoneverificationapp import views
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()
# router.register(r'profile', views.profileDetailview, basename='update')
urlpatterns = [
    path('phone/', views.phonenumberviewset.as_view(), name='phone_no'),
    path('status/', views.phonenumberviews.as_view(), name='verification_status'),
    path('verify/', views.verifyphonenumber, name='verify'),
    path('profile/', views.profileDetailview.as_view(), name='update'),

]
urlpatterns += router.urls
