from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, permissions, mixins
from knox.auth import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import servicemodel, stylemodel, offermodel, stylistmodel, bookmodels
from .serializers import offermodelserializers, \
    readonlystylemodelserialzers, writestylemodelserialzers, readservicemodelserializers, writeservicemodelserializers, \
    stylistmodelserializers, writebookserviceserializers, readbookingserializer


class serviceviewset(ModelViewSet):
    queryset = servicemodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return readservicemodelserializers
        return writeservicemodelserializers

    def get_permissions(self):
        if self.action == 'list' and self.request.user.is_active:
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()


class styleviewset(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ] # Will only be visible to admin upon deployment 
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return stylemodel.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return readonlystylemodelserialzers
        return writestylemodelserialzers


class offerviewset(ModelViewSet):
    serializer_class = offermodelserializers
    queryset = offermodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PageNumberPagination


class stylistviewset(ModelViewSet):
    serializer_class = stylistmodelserializers
    queryset = stylistmodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PageNumberPagination


class bookingsviewset(ModelViewSet):
    """bookings"""
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):
        return bookmodels.objects.prefetch_related("user_detail", 'service', "stylist").filter(user_detail=self.request.user).order_by("service_Time")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return readbookingserializer
        return writebookserviceserializers

    def perform_create(self, serializer):
        '''Associate user with phone number'''
        serializer.save(user_detail=self.request.user)


class service_style_view(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    pagination_class = PageNumberPagination
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_objects(self, pk1):
        try:
            return stylemodel.objects.filter(service_picture=str(pk1))
        except stylemodel.DoesNotExist:
            raise Http404

    def get_object(self, pk1, pk2):
        try:
            return stylemodel.objects.get(service_picture=pk1, pk=pk2)
        except stylemodel.DoesNotExist:
            raise Http404

    def get(self, request, pk1, pk2=None, format=None):
        if pk1 and pk2:
            snippet = self.get_object(pk1, pk2)
            serializer = readonlystylemodelserialzers(snippet)
        elif pk1:
            snippet = self.get_objects(pk1)

            serializer = readonlystylemodelserialzers(snippet, many=True)
        return self.get_paginated_response(serializer.data)