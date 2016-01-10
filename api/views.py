from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from activities.models import Act
from common.models import MyUser
from post.models import Post
from comment.models import Comment
from .serializers import ActSerializer, PostAllSerializer, PostSerializer, UserSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class ActList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Act.objects.all()
        act_type = self.request.query_params.get('act_type', None)
        if act_type is not None:
            queryset = queryset.filter(act_type=act_type)
        return queryset

class PostAllList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostAllSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

 
class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given post_id,
        by filtering against a `post_id` query parameter in the URL.
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        if post_id is not None:
            queryset = queryset.filter(id=post_id)
        return queryset



class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer



