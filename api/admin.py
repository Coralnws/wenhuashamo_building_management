from django.contrib import admin
from .models import *

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username','real_name' ,'email')

class ScholarsAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name','email')

class CodeAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'code','sendTo')

class InstituteAdminConfig(admin.ModelAdmin):
    list_display = ('id','name')

class FieldAdminConfig(admin.ModelAdmin):
    list_display = ('id','title')

class UserScholarConfig(admin.ModelAdmin):
    list_display = ('id', 'isFollow', 'user_id', 'scholar_id')

class UserRequestScholarConfig(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'scholar_id')

class UserAuthenticateScholarConfig(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'scholar_id')

class UserAuthenticateArticleConfig(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'article_id')

class ReportConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'result', 'category', 'reportArticle_id', 'reportScholar_id')

admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Scholar, ScholarsAdminConfig)
admin.site.register(Code, CodeAdminConfig)
admin.site.register(Institute, InstituteAdminConfig)
admin.site.register(AcademicField, FieldAdminConfig)
admin.site.register(UserScholar)
admin.site.register(UserRequestScholar)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Report, ReportConfig)
admin.site.register(UserArticle)
admin.site.register(History)
admin.site.register(Review)
admin.site.register(UserAuthenticateArticle, UserAuthenticateArticleConfig)
admin.site.register(UserAuthenticateScholar, UserAuthenticateScholarConfig)
