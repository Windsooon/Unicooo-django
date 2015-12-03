from django.forms import widgets
from rest_framework import serializers
from .models import Act 
from .choices import ACTTYPE, ACTLICENCE


class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ("id", "user", "act_title", "act_content", "act_thumb_url", 
                  "act_ident", "act_type", "act_licence", "act_star", "act_status",
                  "act_url", "act_delete", "act_create_time")

