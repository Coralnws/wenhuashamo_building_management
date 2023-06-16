from django.urls import path

from api.views import userManage

urlpatterns = [

    # User Authentication
    path('user/login', userManage.login),
    path('user/logout', userManage.logout),


]