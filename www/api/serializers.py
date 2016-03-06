from django.forms import widgets
from rest_framework import serializers
from activities.models import Act 
from common.models import MyUser
from post.models import Post
from comment.models import Comment
from activities.choices import ACTTYPE, ACTLICENCE


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id",  "email", "password", "user_name", "user_avatar", "user_gender", "user_point", "user_details")
        extra_kwargs = {
                "password": {"write_only": True},
                "email": {"write_only": True}
        }
        read_only_fields = ("id", "user_avatar", "user_details", "user_gender", "user_point")

    def create(self, validated_data):
        user = MyUser.objects.create(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("user_gender", "user_details")
        #read_only_fields = ("id", "user_avatar", "user_details", "user_gender", "user_point")

class ActSerializer(serializers.ModelSerializer):
    """Activity api fields"""
    act_user = UserSerializer(source="user", read_only=True)
    act_author = serializers.ReadOnlyField(source='user.user_name')


    class Meta:
        model = Act
        fields = ("id", "act_author", "act_title", "act_content", "act_thumb_url", 
                  "act_ident", "act_type", "act_licence", "act_star", "act_status",
                  "act_url", "act_delete", "act_create_time", "act_user")


class CommentSerializer(serializers.ModelSerializer):
    """Comment api fields"""
    comment_user = UserSerializer(source="user", read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
    comment_author = serializers.ReadOnlyField(source='user.user_name')
    comment_avatar = serializers.ReadOnlyField(source='user.user_avatar')

    class Meta:
        model = Comment
        fields = ("id", "user", "comment_author", "comment_avatar", "post", "reply_id", "comment_content", "comment_create_time","comment_user")
        

class PostAllSerializer(serializers.ModelSerializer):
    """Posts api fields"""
    post_user = UserSerializer(source="user", read_only=True)
    post_author = serializers.ReadOnlyField(source='user.user_name')
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "act", "post_author", "post_title", "post_content", "post_thumb_url", "post_thumb_width", "post_thumb_height", "nsfw", "post_create_time", "post_user", "comment_count") 
       
    def get_comment_count(self, obj):
        return obj.comment_post.count()
       
class PostSerializer(serializers.ModelSerializer):
    """Post api fields"""
    post_comment = CommentSerializer(many=True, source="comment_post")
    post_user = UserSerializer(source="user")

    class Meta:
        model = Post
        fields = ("id", "user", "post_title", "post_content", "post_thumb_url", "post_create_time", "post_user", "post_comment") 





