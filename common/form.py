#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_signup',
                'class': 'form-control',
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
                    'minlength': 6,
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'id': 'email_signup',
                    'class': 'form-control',
                    'minlength': 8,
                }
            ),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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

    def clean_password(self):
        return self.initial["password"]


