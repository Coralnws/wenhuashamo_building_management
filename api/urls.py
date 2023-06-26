from django.urls import path

from api.views import rentApi
from api.views import userApi
from api.views import staffManagemntApi
from api.views import paymentManageApi
from api.views import messageManage
from api.views import houseInspect
from api.views import maintenanceApi
from api.views import visitRequestApi
from api.views import statisticApi
from api.views import libraryManage
from api.views import sms
from api.scheduler import sms_reminder, email_reminder


urlpatterns = [

    # User Authentication
    path('user/login', userApi.login),
    path('user/logout', userApi.logout),
    path('user/change_password', userApi.change_password),
    path('user/create', staffManagemntApi.create_user),


    path('rent/create', rentApi.rent_create),
    path('rent/detailRead', rentApi.rent_detail_read),
    path('rent/update', rentApi.rent_update),
    path('rent/delete', rentApi.rent_delete),
    path('rent/user/detail', rentApi.rent_user_detail_read),

    #Staff Management
    path('staff/createStaff', staffManagemntApi.create_staff),
    path('staff/updateStaff', staffManagemntApi.update_staff),
    path('staff/delStaff', staffManagemntApi.delete_staff),
    path('staff/getStaff', staffManagemntApi.get_staff),
    

    #Management Fee
    path('payment/updateRecord', paymentManageApi.update_record),

    #Tenant Management
    path('tenant/add_tenant',    messageManage.add_tenant),
    path('tenant/delete_tenant', messageManage.delete_tenant),
    path('tenant/update_tenant', messageManage.update_tenant),
    path('tenant/view_tenant',   messageManage.view_tenant),
    path('tenant/search_tenant', messageManage.search_tenant),

    #Repair
    path('repair/createRequest', maintenanceApi.create_request),
    path('repair/getRequest', maintenanceApi.get_request),
    path('repair/assignTask', maintenanceApi.assign_task),
    path('repair/closeTask', maintenanceApi.close_task),
    #path('repair/updateRequest', maintenanceApi.update_request),
    path('repair/delRequest', maintenanceApi.del_request),
    path('repair/timeslot', maintenanceApi.get_timeslot),
    path('repair/save', maintenanceApi.save_library),
    
    #Visit
    path('visit/create', visitRequestApi.create_request),
    path('visit/update', visitRequestApi.update_request),
    path('visit/delete', visitRequestApi.del_request),
    path('visit/get', visitRequestApi.get_request),

    #statistic
    path('statistic/repair', statisticApi.repair_statistic),
    path('statistic/repair_year', statisticApi.repair_statistic_year),
    path('statistic/visit', statisticApi.visit_statistic_month),


    #House Inspect
    path('house_inspect', houseInspect.house_list_by_floor),
    path('house_company', houseInspect.get_company_house),

    #library
    path('library', libraryManage.get_library),
    path('resend_otp', sms.resend_otp),

]