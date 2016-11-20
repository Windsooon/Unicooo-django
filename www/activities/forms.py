from django import forms
from .models import Act


class ActCreateForm(forms.ModelForm):
    class Meta:
        model = Act
        fields = ("act_title", "act_content", "act_type",)
        labels = {
            "act_title": "Activitiy Title",
            "act_content": "Activitiy Content",
            "act_type": "Activitiy Type",
        }
        widgets = {
            "act_title": forms.TextInput(
                attrs={
                    "id": "act_title",
                    "class": "form-control",
                    "minlength": 6,
                }
            ),
            "act_content": forms.Textarea(
                attrs={
                    "id": "act_content",
                    "class": "form-control",
                    "minlength": 6,
                }
            ),
            "act_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }
