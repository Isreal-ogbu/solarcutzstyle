from account import views
from django.urls import path
from knox import views as knox_views
from rest_framework import routers

from account.views import usersview, profilepictureview

router = routers.SimpleRouter()

router.register(r"users", usersview, basename='users')

urlpatterns = [
   path('register/', views.register_api.as_view(), name='register'),
   path('login/', views.login_api.as_view(), name='login'),
   path('logout/',  knox_views.LogoutView.as_view(), name='logout'),
   path('pp/',  views.profilepictureview.as_view(), name='logout'),
   ] + router.urls
