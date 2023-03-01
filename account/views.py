from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .models import userdetails

from .serializers import userRegistrationSerializer, logindetailsserializers, userdetailsserializers, \
    profilepictureserializers


class register_api(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = userRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Registration Successfull...!", "status": 200})


class login_api(generics.GenericAPIView):
    serializer_class = logindetailsserializers

    """ A csrf token will not be submitted as a result of no authentication """

    @csrf_exempt
    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None and not user.is_staff:
            try:
                obj = userdetails.objects.get(owner=user)
            except userdetails.DoesNotExist:
                obj = None
            token = AuthToken.objects.create(user)[1]
            obj = userdetailsserializers(obj)
            if obj.data['userprofilepicture'] is not None:
                userprofilepicture = "127.0.0.1" + obj.data['userprofilepicture']
            else:
                userprofilepicture = "https://cdn0.iconfinder.com/data/icons/user-pictures/100/unknown_1-2-512.png"
            obj = {
                'username': user.username,
                'profile': userprofilepicture,
            }
            if obj['profile'] is None:
                pass
            request.session['current_user'] = user.id
            return Response({"msg": "Login Successfull...!", "token": token,
                             "user": obj, "status": 200})
        else:
            return Response({
                "msg": "User Not Found...!"
            }, 404)


class usersview(ReadOnlyModelViewSet):
    """This view is only to be seen by the admin"""
    serializer_class = profilepictureserializers
    queryset = userdetails.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [TokenAuthentication, ]


class profilepictureview(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    """
        Retrieve, update or delete a snippet instance.
        """

    def get_object(self, pk):
        try:
            return userdetails.objects.get(owner=pk)
        except userdetails.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        pic = self.get_object(request.user)
        serializer = profilepictureserializers(pic)
        return Response(serializer.data)

    def put(self, request, format=None):
        pic = self.get_object(request.user)
        print(type(request.data))
        serializer = profilepictureserializers(pic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, format=None):
    #     pic = self.get_object(request.user)
    #     serializer = profilepictureserializers(pic, data='')
    #     if serializer.is_valid():
    #         serializer.save(commit=False)
    #         serializer.data["userprofilepicture"] = None
    #         serializer.save()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
