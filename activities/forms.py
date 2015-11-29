from django import forms

class ActForm(forms.ModelForm):
    class Meta:
        model = Act
        fields = ("act_title", "act_content",)
        labels = {
            "act_title": "Activitiy Title", 
            "act_content": "Activitiy Content", 
        }
        widgets = {
            'act_title': forms.TextInput(
                attrs={
                    'id': 'act_title',
                    'class': 'form-control',
                    'placeholder': 'Please ender your activity title',
                    'minlength': 3,
                }
            ),
            'act_content': forms.TextInput(
                attrs={
                    'id': 'act_content',
                    'class': 'form-control',
                    'placeholder': 'Please ender your activity content',
                    'minlength': 15,
                }
            ),
        }

