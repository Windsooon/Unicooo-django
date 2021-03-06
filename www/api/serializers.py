from activities.models import Act
from django.core.cache import cache
from common.models import MyUser
from post.models import Post
from comment.models import Comment
from .base import text_contain_xss

# Django rest-framework
from rest_framework import serializers

# Django-redis
from django_redis import get_redis_connection


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = (
            "id",  "email", "password", "user_name", "user_details")
        extra_kwargs = {
            "email": {"write_only": True},
            "password": {"write_only": True}}
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = MyUser.objects.create(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_user_name(self, value):
        if not text_contain_xss(value):
            raise serializers.ValidationError(
                "Username may only contain alphanumeric characters.")
        return value


class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            "email", "password", "user_avatar",
            "user_gender", "user_details")
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"write_only": True, "required": False}}
        read_only_fields = ("id",)


class ActSerializer(serializers.ModelSerializer):
    """Activity api fields"""
    act_user = UserSerializer(source="user", read_only=True)
    act_author = serializers.ReadOnlyField(source='user.user_name')
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Act
        fields = (
                "id", "act_author", "act_title", "act_content", "likes",
                "act_thumb_url", "act_type", "act_licence", "act_intro",
                "act_star", "act_status", "act_url", "act_delete",
                "act_create_time", "act_user"
        )

    def get_likes(self, obj):
        act_id = obj.id
        likes = cache.get("act_"+str(act_id))
        if likes is None:
            return 0
        else:
            return likes

    def validate_act_title(self, value):
        if not text_contain_xss(value):
            raise serializers.ValidationError(
                "Act content may only contain alphanumeric characters.")
        return value

    def validate_act_content(self, value):
        if not text_contain_xss(value):
            raise serializers.ValidationError(
                "Act content may only contain alphanumeric characters.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Comment api fields"""
    comment_user = UserSerializer(source="user", read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
    comment_author = serializers.ReadOnlyField(source='user.user_name')

    class Meta:
        model = Comment
        fields = (
                "id", "user", "comment_author", "post",
                "reply_id", "comment_content",
                "comment_create_time", "comment_user"
        )

    def validate_comment_content(self, value):
        if not text_contain_xss(value):
            raise serializers.ValidationError(
                "Comment may only contain alphanumeric characters.")
        return value


class PostAllSerializer(serializers.ModelSerializer):
    """Posts api fields"""
    post_user = UserSerializer(source="user", read_only=True)
    act_type = serializers.ReadOnlyField(source='act.act_type')
    post_author = serializers.ReadOnlyField(source='user.user_name')
    comment_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
                "id", "act", "act_type", "likes", "post_author",
                "post_title", "post_content", "post_url", "post_thumb_url",
                "post_thumb_width", "post_thumb_height",
                "post_mime_types", "nsfw", "post_create_time",
                "post_user", "comment_count"
        )

    def validate_post_content(self, value):
        if not text_contain_xss(value):
            raise serializers.ValidationError(
                "Post content may only contain alphanumeric characters.")
        return value

    def get_comment_count(self, obj):
        return obj.comment_post.count()

    def get_likes(self, obj):
        post_id = obj.id
        post_likes_users = get_redis_connection("default")
        likes = post_likes_users.zcard("post_"+str(post_id))
        if likes is None:
            return 0
        else:
            return likes


class PostSerializer(serializers.ModelSerializer):
    """Post api fields"""
    post_comment = CommentSerializer(
        many=True, source="comment_post", required=False)
    post_user = UserSerializer(source="user", required=False)
    comment_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
                "id", "user", "post_title", "post_content",
                "likes", "post_thumb_url", "post_url", "post_thumb_width",
                "post_thumb_height", "post_mime_types",
                "post_create_time", "post_user", "comment_count",
                "post_comment"
        )

    def get_likes(self, obj):
        post_id = obj.id
        post_likes_users = get_redis_connection("default")
        likes = post_likes_users.zcard("post_"+str(post_id))
        if likes is None:
            return 0
        else:
            return likes

    def get_comment_count(self, obj):
        return obj.comment_post.count()
