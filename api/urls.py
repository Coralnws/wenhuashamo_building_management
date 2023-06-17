from django.urls import path

from api.views import userManage
from api.views import managerApi
from api.views import paymentManageApi

urlpatterns = [

    # User Authentication
    path('user/login', userManage.login),
    path('user/logout', userManage.logout),



    #Staff Management
    path('staff/createStaff', managerApi.createStaff),
    path('staff/updateStaff', managerApi.updateStaff),
    path('staff/delStaff', managerApi.deleteStaff),
    path('staff/getStaff', managerApi.getStaff),

    #Management Fee


]