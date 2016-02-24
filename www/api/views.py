from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.db.models import Max
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from activities.models import Act
from common.models import MyUser
from post.models import Post
from comment.models import Comment
from .serializers import ActSerializer, PostAllSerializer, PostSerializer, UserSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthenticatedOrCreate


class ActList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Act.objects.all().order_by('id')
        act_type = self.request.query_params.get('act_type', None)
        act_id = self.request.query_params.get('id', None)
        if act_type is not None:
            queryset = queryset.filter(act_type=act_type)
        if act_id is not None:
            queryset = queryset.filter(user_id=act_id)
        return queryset

class ActDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostAllSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        act_id = self.request.query_params.get('act_id', None)
        if act_id is not None:
            queryset = queryset.filter(act=act_id)
        return queryset


 
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        act_id = self.request.query_params.get('act_id', None)
       
        if act_id is not None:
            queryset = queryset.filter(act=act_id)

        return queryset


class CommentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        new_user = authenticate(email=request.POST.get('email'),
            password=request.POST.get('password'),
            )
        if new_user is not None:
            if new_user.is_active:
                django_login(request, new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

