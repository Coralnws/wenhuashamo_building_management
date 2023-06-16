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

    CATEGORY = (
        (1, '普通用户'),
        (2, '学者'),
    )

    QUESTION = (
        ('1','您最喜欢的颜色？'),
        ('2','您最讨厌的食物？'),
        ('3','您最要好的闺蜜/兄弟？'),
        ('4','您的爱好？'),
        ('5','您的初恋？'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    real_name = models.CharField(max_length=150,blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, default = "A bio hasn't been added yet.")
    is_staff = models.BooleanField(default=False)
    # activated at email validation only, not at registration.
    is_active = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GENDER, default=GENDER[0][0])
    dob = models.DateField(default=datetime.date(2000, 1, 1))
    wbId = models.CharField(max_length=150,blank=True)
    vxId = models.CharField(max_length=150,blank=True)
    qqId = models.CharField(max_length=150,blank=True)
    profile = models.ImageField(upload_to=profile_to, blank=True)
    thumbnail = models.ImageField(upload_to=thumbnail_to, blank=True)
    
    position = models.CharField(max_length=150,blank=True)
    securityQuestion=models.CharField(max_length=1,choices=QUESTION,default='1')
    securityAnswer=models.CharField(max_length=150,blank=True)
    identity = models.IntegerField(choices=CATEGORY,default=0)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    scholarAuth = models.CharField(max_length=40 ,blank=True,null=True)
    banComment = models.BooleanField(default=False)
    banDuration = models.DateTimeField(blank=True,null=True,default=None)

    def get_thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return os.path.join(MEDIA_URL, str(self.thumbnail))
        return os.path.join(MEDIA_URL, 'default', 'thumbnail.png')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email',]

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
