from django.urls import path

from api.views import userManage
from api.views.messageManage import add_tenant, delete_tenant, update_tenant, view_tenant

urlpatterns = [

    # User Authentication
    path('user/login', userManage.login),
    path('user/logout', userManage.logout),
    path('add_tenant', add_tenant),
    path('delete_tenant', delete_tenant),
    path('update_tenant', update_tenant),
    path('view_tenant', view_tenant),

]