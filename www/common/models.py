from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
from activities.choices import USERGENDER
from django.core.cache import cache


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """ 通过邮箱创建用户 """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_name=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        if kwargs:
            if kwargs.get('is_active', None):
                user.is_active = kwargs['is_active']
            if kwargs.get('is_admin', None):
                user.is_admin = kwargs['is_admin']
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        创建公司管理员
        """
        user = self.create_user(
            username="admin_username",
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = 1
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
            verbose_name='Email Address',
            max_length=255,
            unique=True
            )
    user_name = models.CharField(max_length=30, unique=True)
    user_avatar = models.CharField(max_length=255, blank=True)
    user_gender = models.IntegerField(
            choices=USERGENDER,
            default=USERGENDER[0][0]
            )
    user_details = models.CharField(max_length=80)
    user_register_time = models.DateTimeField(auto_now=True)
    user_validated = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def replace_html(self, text):
        return str(text).replace('&', '&amp;').replace('<', '&lt;') \
            .replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def points(self):
        '''
        get user points
        '''
        return cache.get("user_points_"+str(self.id))

    class Meta:
        db_table = 'common_user'


class CustomAuth(object):
    """自定义用户验证"""
    def authenticate(self, email=None, password=None):
        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except MyUser.DoesNotExist:
            return None
