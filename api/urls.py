from django.urls import path

from api.views import rentApi
from api.views import userApi
from api.views import staffManagemntApi
from api.views import paymentManageApi
from api.views import messageManage
from api.views import houseInspect

urlpatterns = [

    # User Authentication
    path('user/login', userApi.login),
    path('user/logout', userApi.logout),


    path('rent/create', rentApi.rentCreate),
    path('rent/detailRead', rentApi.rentDetailRead),
    path('rent/update', rentApi.rentUpdate),
    path('rent/user/detail', rentApi.rentUserDetailRead),

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
    path('payment/getPaymentDetail', paymentManageApi.getPaymentDetail),

    #Tenant Management
    path('tenant/add_tenant',    messageManage.add_tenant),
    path('tenant/delete_tenant', messageManage.delete_tenant),
    path('tenant/update_tenant', messageManage.update_tenant),
    path('tenant/view_tenant',   messageManage.view_tenant),
    path('tenant/search_tenant', messageManage.search_tenant),

    #House Inspect
    path('house_inspect', houseInspect.house_list_by_floor),

]