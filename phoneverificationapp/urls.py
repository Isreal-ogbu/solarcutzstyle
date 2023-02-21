from phoneverificationapp import views
from django.urls import path
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'update', views.profileviewset, basename='update')
urlpatterns = [
    path('phone/', views.phonenumberviewset.as_view(), name='phone_no'),
    path('status/', views.phonenumberviews.as_view(), name='verification_status'),
    path('verify/', views.verifyphonenumber, name='verify'),
    # path('update/', views.profileviewset, name='update'),

]
urlpatterns += router.urls
