from django.shortcuts import render
from rest_framework import generics, permissions, mixins
from knox.auth import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import servicemodel, stylemodel, offermodel, stylistmodel, bookmodels
from .serializers import offermodelserializers, \
    readonlystylemodelserialzers, writestylemodelserialzers, readservicemodelserializers, writeservicemodelserializers, \
    stylistmodelserializers, writebookserviceserializers, readbookingserializer


class serviceviewset(ModelViewSet):
    queryset = servicemodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return readservicemodelserializers
        return writeservicemodelserializers

    # def list(self, request, *args, format=None, **kwargs):
    #     user_count = servicemodel.objects.all()
    #     results = readservicemodelserializers(user_count, many=True)
    #     return Response(results.data)


class styleviewset(ModelViewSet):
    queryset = stylemodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return readonlystylemodelserialzers
        return writestylemodelserialzers

    # def list(self, request, *args, format=None, **kwargs):
    #     user_count = stylemodel.objects.all()
    #     results = readonlystylemodelserialzers(user_count, many=True)
    #     return Response(results.data)


class offerviewset(ModelViewSet):
    serializer_class = offermodelserializers
    queryset = offermodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = PageNumberPagination

    # def list(self, request, *args, format=None, **kwargs):
    #     user_count = offermodel.objects.all()
    #     results = offermodelserializers(user_count, many=True)
    #     return Response(results.data)


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
        return bookmodels.objects.filter(user_detail=self.request.user).order_by("service_Time")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return readbookingserializer
        return writebookserviceserializers

    def perform_create(self, serializer):
        '''Associate user with phone number'''
        serializer.save(user_detail=self.request.user)

