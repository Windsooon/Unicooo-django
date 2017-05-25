#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_signup',
                'class': 'form-control',
                'maxlength': 40,
                'minlength': 8,
            }
        )
    )

    class Meta:
        model = MyUser
        fields = ('user_name', 'email')
        labels = {
            'user_name': 'username',
            'email': 'eamil',
            'password': 'password',
        }
        widgets = {
            'user_name': forms.TextInput(
                attrs={
                    'id': 'username_signup',
                    'class': 'form-control',
                    'maxlength': 30,
                    'minlength': 6,
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'id': 'email_signup',
                    'class': 'form-control',
                    'maxlength': 255,
                    'minlength': 8,
                }
            ),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'id': 'email_login',
                'class': 'form-control',
                'minlength': 8,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_login',
                'class': 'form-control',
                'minlength': 8,
            }
        )
    )

    class Meta:
        model = MyUser
        fields = ('email',)


# 修改用户表单
class UserChangeForm(forms.ModelForm):
    """A form for change user"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = "__all__"
        labels = {
                "user_gender": "User Gender",
                "user_details": "User Details"
        }
        widgets = {
            "user_gender": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "user_details": forms.TextInput(
                attrs={
                    "id": "user-details",
                    "class": "form-control",
                    "minlength": 10,
                }
            ),
        }

    def clean_password(self):
        return self.initial["password"]
