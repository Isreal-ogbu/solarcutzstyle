import time

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet

from .serializers import phoneverificationserializers, phonelistserializers, userprofileserializers
from .models import phonenumbermodel
from rest_framework.response import Response
from .verify import check


class phonenumberviewset(CreateAPIView):
    """phone/"""
    serializer_class = phoneverificationserializers
    queryset = phonenumbermodel.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def perform_create(self, serializer):
        '''Associate user with phone number'''
        serializer.save(owner=self.request.user)


class phonenumberviews(ListAPIView):
    """status/"""
    """List out all unverified and verified phone number of a particular user"""
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def list(self, request, *args, format=None, **kwargs):
        user_count = phonenumbermodel.objects.filter(owner=self.request.user)
        results = phonelistserializers(user_count, many=True)
        return Response(results.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def verifyphonenumber(request):
    """To verify otp service"""
    if request.method == "POST":
        code = request.data['key']
        if len(str(code)) < 6 or len(str(code)) > 6 or str(code).isalpha():
            return Response({"status": "invalid"}, 300)
        user = phonenumbermodel.objects.get(owner=request.user)
        if check(user.phonenumber, code):
            user.verifiednumber = True
            user.save()
            return Response({"msg": "Successful", "status": 200})
        else:
            return Response({"msg": "UnSuccessful", "status": 422})


class profileviewset(ModelViewSet):
    serializer_class = userprofileserializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        return phonenumbermodel.objects.filter(owner=self.request.user)

