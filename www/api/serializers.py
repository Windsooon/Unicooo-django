from django.forms import widgets
from rest_framework import serializers
from activities.models import Act 
from common.models import MyUser
from post.models import Post
from comment.models import Comment
from activities.choices import ACTTYPE, ACTLICENCE

class UserSerializer(serializers.ModelSerializer):
    """User api fields"""
    class Meta:
        model = MyUser
        fields = ("id", "last_login","user_name", 
                  "user_avatar", "user_gender", "user_point", "user_details", "user_register_time",
                  "is_active", "is_admin")

        
class ActSerializer(serializers.ModelSerializer):
    """Activity api fields"""
    act_user = UserSerializer(source="user")
    user = serializers.ReadOnlyField(source='user.user_name')

    class Meta:
        model = Act
        fields = ("id", "user","act_title", "act_content", "act_thumb_url", 
                  "act_ident", "act_type", "act_licence", "act_star", "act_status",
                  "act_url", "act_delete", "act_create_time", "act_user")


class PostAllSerializer(serializers.ModelSerializer):
    """Posts api fields"""
    post_user = UserSerializer(source="user")

    class Meta:
        model = Post
        fields = ("id", "user", "act","post_title", "post_content", "post_thumb_url", "post_create_time", "post_user") 


class CommentSerializer(serializers.ModelSerializer):
    """Comment api fields"""
    comment_user = UserSerializer(source="user", read_only=True)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Comment
        fields = ("id", "user", "post", "reply_id", "comment_content", "comment_create_time","comment_user")
        
        
class PostSerializer(serializers.ModelSerializer):
    """Post api fields"""
    post_comment = CommentSerializer(many=True, source="comment_post")
    post_user = UserSerializer(source="user")

    class Meta:
        model = Post
        fields = ("id", "user", "post_title", "post_content", "post_thumb_url", "post_create_time", "post_user", "post_comment") 





