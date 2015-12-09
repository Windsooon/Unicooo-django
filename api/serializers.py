from django.forms import widgets
from rest_framework import serializers
from activities.models import Act 
from common.models import MyUser
from post.models import Post
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
        fields = ("id", "user", "act_user", "act_title", "act_content", "act_thumb_url", 
                  "act_ident", "act_type", "act_licence", "act_star", "act_status",
                  "act_url", "act_delete", "act_create_time")


class PostSerializer(serializers.ModelSerializer):
    """Post api fields"""
    post_user = UserSerializer(source="user")

    class Meta:
        model = Post
        fields = ("id", "user", "post_user", "post_title", "post_content", "post_thumb_url") 




