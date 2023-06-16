import uuid
from django.db import models
from django.utils import timezone
import datetime
import os
import random
import uuid

from backend.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    # Method for creating normal user
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        newUser = self.model(email=email, username=username, **other_fields)
        newUser.set_password(password)
        newUser.save()
        return newUser

    # Method for creating superuser
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff = True."))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser = True."))

        return self.create_user(email, username, password, **other_fields)

# 让上传的文件路径动态地与user的名字有关
def thumbnail_to(instance, filename):
    return os.path.join('user', instance.email, str(random.uniform(1000, 9999)) + 'thumbnail.png')

def profile_to(instance, filename):
    return os.path.join('user', instance.email, str(random.uniform(1000, 9999)) + 'profile.png')


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ('O', 'Prefer Not to Say'),
        ('M', 'Male'),
        ('F', 'Female'),
    )

    POSITION = (
        ('1','普通用户'),
        ('2','维修人员'),
        ('3','普通管理员'),
        ('4','超级管理员'),
    )

    M_TYPE = (
        ('0','无'),
        ('1','水'),
        ('2','电'),
        ('3','机械'),
    )

    M_STATUS = (
        ('0','可用'),
        ('1','不可用'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    realname = models.CharField(max_length=255,blank=True)
    contactNumber = models.CharField(max_length=255,blank=True)
    position=models.CharField(max_length=1,choices=POSITION,default=POSITION[0][0])
    email = models.EmailField(blank=True)
    bio = models.TextField(max_length=500, default = "这个人很懒，这么久都还没填写信息")
    gender = models.CharField(max_length=10, choices=GENDER, default=GENDER[0][0])
    m_type = models.CharField(max_length=10, choices=M_TYPE, default=M_TYPE[0][0])
    m_status = models.CharField(max_length=10, choices=M_STATUS, default=M_STATUS[0][0])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    isDeleted = models.BooleanField(default=False)
    dob = models.DateField(default=datetime.date(2000, 1, 1))
    profile = models.ImageField(upload_to=profile_to, blank=True)
    thumbnail = models.ImageField(upload_to=thumbnail_to, blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    
    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return os.path.join(MEDIA_URL, str(self.thumbnail))
        return os.path.join(MEDIA_URL, 'default', 'thumbnail.png')


    def get_profile_url(self):
        if self.profile and hasattr(self.profile, 'url'):
            return os.path.join(MEDIA_URL, str(self.profile))
        return os.path.join(MEDIA_URL, 'default', 'profile.png')


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    # class Meta:
    #     app_label = 'api'

    def __str__(self):
        return f'{self.username} ({self.id})'

    def has_perm(self, perm, obj=None):
        """
        A method used to check if the user has permission
        """
        return True

    def tokens(self):
        """
        A method used to get the token of user
        """
        return get_tokens(self)

    def set_password(self, raw_password):
        self.password = make_password(raw_password,"a","pbkdf2_sha1")
        self._password = raw_password
