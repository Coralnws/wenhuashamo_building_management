from django.contrib import admin
from .models import *

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'realname','email', 'profile')

admin.site.register(CustomUser, UserAdminConfig)