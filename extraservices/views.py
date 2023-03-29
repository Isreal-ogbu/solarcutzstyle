from django.shortcuts import render
from .serializers import ideaserializers, contactserializers
from rest_framework.viewsets import ModelViewSet
from .models import idea_suggestionmodel, contact_supportmodel
from knox.auth import TokenAuthentication
from rest_framework import permissions


# Create your views here.

class ideagenerationviewset(ModelViewSet):
    serialiazer_class = ideaserializers
    queryset = idea_suggestionmodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = None
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.action == 'create' and self.request.user.is_active:
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()


class contactviewset(ModelViewSet):
    serialiazer_class = contactserializers
    queryset = contact_supportmodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = None
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.action == 'create' and self.request.user.is_active:
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()
