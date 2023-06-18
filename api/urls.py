from django.urls import path

from api.views import userManage
from api.views import staffManagemntApi
from api.views import paymentManageApi

urlpatterns = [

    # User Authentication
    path('user/login', userManage.login),
    path('user/logout', userManage.logout),


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

]