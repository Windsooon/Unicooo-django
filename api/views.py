from django.shortcuts import render
from ..activities.models import Act
from .serializers import ActSerializer
from rest_framework import generics


class ActList(generics.ListCreateAPIView):
    queryset = Act.objects.all()
    serializer_class = ActSerializer

