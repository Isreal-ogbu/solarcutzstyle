import time

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets, permissions, mixins, status
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import phoneverificationserializers, phonelistserializers, userprofileserializers, Userserializers, tokenSerializers
from .models import phonenumbermodel
from rest_framework.response import Response
from .verify import check


class phonenumberviewset(ListCreateAPIView):
    """phone/"""
    serializer_class = phoneverificationserializers
    queryset = phonenumbermodel.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    pagination_class = None

    def perform_create(self, serializer):
        '''Associate user with phone number'''
        serializer.save(owner=self.request.user)

    def list(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

class phonenumberviews(ListAPIView):
    """status/"""
    """List out all unverified and verified phone number of a particular user"""
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def list(self, request, *args, format=None, **kwargs):
        user_count = phonenumbermodel.objects.filter(owner=self.request.user)
        results = phonelistserializers(user_count, many=True)
        return Response(results.data)


@api_view(["POST", "GET"])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([TokenAuthentication, ])
def verifyphonenumber(request):
    """To verify otp service"""
    if request.method == "POST":
        print(request.data)
        serializer = tokenSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["token"]
        if not code:
            raise ValueError('Users Must Have an otp code')
        if len(str(code)) < 6 or len(str(code)) > 6 or type(code) == "Integer":
            return Response({"status": "invalid"}, 300)
        user = phonenumbermodel.objects.get(owner=request.user)
        if check(user.phonenumber, code):
            print(user.phonenumber, code)
            user.verifiednumber = True
            user.save()
            return Response({"msg": "Successful", "status": 200})
        else:
            return Response({"msg": "UnSuccessful", "status": 422})
    elif request.method == "GET":
        return Response(status=status.HTTP_200_OK)


# class profileviewset(ModelViewSet):
#     serializer_class = Userserializers
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = [permissions.IsAuthenticated, ]
#     pagination_class = None
#
#     def get_queryset(self):
#         print(self.request.user.username)
#         return User.objects.get(username=self.request.user.username)


class profileDetailview(APIView):
    """profile/"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    """
    Retrieve, update or delete a profile instance.
    """

    def get_object(self, username, pk):
        try:
            return User.objects.get(username=username, pk=pk)
        except User.DoesNotExist:
            raise Http404

    def check_user(self, user):
        try:
            User.objects.get(username=user)
            return Response({"msg": "username already exist", "status": 422})
        except User.DoesNotExist:
            pass

    def get(self, request, format=None):
        snippet = self.get_object(request.user.username, request.user.id)
        serializer = Userserializers(snippet)
        return Response(serializer.data)

    def put(self, request, format=None):
        checker_user = request.data['username']
        self.check_user(checker_user)
        snippet = self.get_object(request.user.username, request.user.id)
        serializer = Userserializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        snippet = self.get_object(request.user.username, request.user.id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
