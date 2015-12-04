from django.forms import widgets
from rest_framework import serializers
from activities.models import Act 
from common.models import MyUser
from activities.choices import ACTTYPE, ACTLICENCE

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MyUser
        fields = ("id", "last_login","user_name", 
                  "user_avatar", "user_gender", "user_point", "user_details", "user_register_time",
                  "is_active", "is_admin")

        
class ActSerializer(serializers.ModelSerializer):
    act_user = UserSerializer(source="user")
    user = serializers.ReadOnlyField(source='user.user_name')

    class Meta:
        model = Act
        fields = ("id", "user", "act_user", "act_title", "act_content", "act_thumb_url", 
                  "act_ident", "act_type", "act_licence", "act_star", "act_status",
                  "act_url", "act_delete", "act_create_time")



