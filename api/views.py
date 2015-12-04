from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from activities.models import Act
from common.models import MyUser
from .serializers import ActSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


class ActList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

