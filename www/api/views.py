import operator
import time
import iso8601

from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.csrf import csrf_exempt
from activities.models import Act
from common.models import MyUser
from post.models import Post
from comment.models import Comment

# django rest framework
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import ActSerializer, PostAllSerializer, PostSerializer, \
        UserSerializer, UserModifySerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly, \
        IsAuthenticatedOrCreate, IsOwnerOrAdminOrPostReadOnly, \
        IsActCreatorOrReadOnly

# django rest framework jwt

# django redis
from django.core.cache import cache
from django_redis import get_redis_connection


class ActList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = sorted(
                serializer.data,
                key=lambda d: (
                    d["likes"]+1)/((time.time()-(
                        iso8601.parse_date(d["act_create_time"])).
                        timestamp())/3600)**1.2,
                reverse=True)
            return self.get_paginated_response(serializer_data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_data = sorted(
                serializer.data, key=operator.itemgetter('likes'),
                reverse=True)
        return Response(serializer_data)

    def get_queryset(self):
        queryset = Act.objects.all()
        post_queryset = Post.objects.all()
        act_type = self.request.query_params.get('act_type', None)
        act_author = self.request.query_params.get('act_author', None)
        act_post = self.request.query_params.get('act_post', None)
        act_id = self.request.query_params.get('act_id', None)
        if act_id is not None:
            queryset = queryset.filter(id=act_id)
        if act_type is not None:
            queryset = queryset.all().filter(act_type=act_type)
        if act_author is not None:
            queryset = queryset.filter(user__user_name=act_author)
        if act_post is not None:
            post_object = post_queryset.filter(
                user__user_name=act_post).values_list(
                    'act_id', flat=True).distinct()
            if post_object.count() >= 0:
                queryset = Act.objects.filter(
                    id__in=post_object)
            else:
                queryset = Act.objects.none()
        return queryset


class ActDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsActCreatorOrReadOnly,)
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostAllSerializer

    # sord post by likes number
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = sorted(
                serializer.data,
                key=lambda d: (d["likes"]+1)/((time.time()-(
                    iso8601.parse_date(d["post_create_time"])).
                    timestamp())/3600)**1.5,
                reverse=True)
            return self.get_paginated_response(serializer_data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_data = sorted(
                serializer.data, key=operator.itemgetter('likes'),
                reverse=True)
        return Response(serializer_data)

    def create(self, request, *args, **kwargs):
        act_id = request.data.get('act')
        act = Act.objects.get(pk=act_id)
        if act.act_type == 0:
            if request.user != act.user:
                return Response(status=403)
        return super().create(request, args, kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        act_id = self.request.query_params.get('act_id', None)
        post_author = self.request.query_params.get('post_author', None)
        post_feed = self.request.query_params.get('post_feed', None)
        if act_id is not None:
            queryset = queryset.filter(act=act_id)
        if post_author is not None:
            queryset = queryset.filter(user__user_name=post_author)
        if post_feed is not None:
            act_list = queryset.filter(
                user__user_name=post_feed).values_list('act_id', flat=True)
            queryset = queryset.filter(act__in=act_list)
        return queryset


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrAdminOrPostReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        post_likes_users = get_redis_connection("default")
        if post_likes_users.zscore(
                "post_"+str(serializer.data["id"]),
                "user"+":"+str(request.user.id)):
            seriaDict = {"like_status": 1}
        else:
            seriaDict = {"like_status": 0}
        seriaDict.update(serializer.data)
        return Response(seriaDict)

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

    def create(self, request, *args, **kwargs):
        reply_id = request.data.get("reply_id")
        cache.set(str(reply_id) + "_comments", "True", timeout=None)
        return super().create(request, args, kwargs)

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        reply_id = self.request.query_params.get('reply_id', None)

        if reply_id is not None:
            queryset = queryset.filter(reply_id=reply_id)

        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)

        return queryset


class CommentDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserList(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        new_user = authenticate(
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            )
        if new_user is not None:
            if new_user.is_active:
                django_login(request, new_user)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = MyUser.objects.all()
    serializer_class = UserModifySerializer

    def update(self, request, *args, **kwargs):
        if 'user_name' in request.data.keys():
            return Response(status=403)
        return super().update(request)
