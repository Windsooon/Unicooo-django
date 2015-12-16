from django import forms
from .models import Act
from django.utils.translation import ugettext as _

class ActForm(forms.ModelForm):
    class Meta:
        model = Act
        fields = ("act_title", "act_content", "act_type", "act_licence")
        labels = {
            "act_title": "Activitiy Title", 
            "act_content": "Activitiy Content", 
            "act_type": "Activitiy Type", 
            "act_licence": "Activitiy Licence", 
        }
        widgets = {
            "act_title": forms.TextInput(
                attrs={
                    "id": "act_title",
                    "class": "form-control",
                    "minlength": 3,
                }
            ),
            "act_content": forms.Textarea(
                attrs={
                    "id": "act_content",
                    "class": "form-control",
                    "minlength": 15,
                }
            ),
            "act_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "act_licence": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }

