from django.urls import path

from api.views import userApi
from api.views import staffManagemntApi
from api.views import paymentManageApi
from api.views.houseInspect import house_list_by_floor
from api.views.messageManage import add_tenant, delete_tenant, update_tenant, view_tenant

urlpatterns = [

    # User Authentication
    path('user/login', userApi.login),
    path('user/logout', userApi.logout),


    #Staff Management
    path('staff/createStaff', staffManagemntApi.createStaff),
    path('staff/updateStaff', staffManagemntApi.updateStaff),
    path('staff/delStaff', staffManagemntApi.deleteStaff),
    path('staff/getStaff', staffManagemntApi.getStaff),

    #Management Fee
    path('payment/createRecord', paymentManageApi.createRecord),
    path('payment/delRecord', paymentManageApi.deleteRecord),
    path('payment/updateRecord', paymentManageApi.updateRecord),
    path('payment/updateStatus', paymentManageApi.updatePaymentStatus),
    path('payment/getPayment', paymentManageApi.getPaymentRecord),
    
    path('add_tenant', add_tenant),
    path('delete_tenant', delete_tenant),
    path('update_tenant', update_tenant),
    path('view_tenant', view_tenant),
    path('house_inspect', house_list_by_floor),

]