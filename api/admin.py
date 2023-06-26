from django.contrib import admin
from .models import *

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'realname','position','m_type','email', 'profile','tenant')

class PaymentConfig(admin.ModelAdmin):
    list_display = ('id', 'tenant')

class TenantConfig(admin.ModelAdmin):
    list_display = ('id', 'username','real_name')

class RepairConfig(admin.ModelAdmin):
    list_display = ('id','title','description', 'createdTime','house','company','contactName','submitter','staff', 'time_slot','contactNumber',
                    'staffContact','manager','repairingTime','status','plan','completeTime','solver','type')

class HouseConfig(admin.ModelAdmin):
    list_display = ('id', 'roomNumber', 'floor')

class TimeslotConfig(admin.ModelAdmin):
    list_display = ('id', 'date', 'slot','staff','type','repair_info')

class VisitConfig(admin.ModelAdmin):
    list_display = ('id', 'name', 'ic','visit_time','company','house','inviter','contact_number','otp')
    
class TenantRentalConfig(admin.ModelAdmin):
    list_display = ('id', 'house', 'rental')
        
class LibraryConfig(admin.ModelAdmin):
    list_display = ('id', 'title', 'description','staff_name','staff_contact','solution','type')

class RentalInfoConfig(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'contract_id','startTime', 'endTime','nextRentalDeadline','nextManagementFeeDeadline')


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Payment, PaymentConfig)
admin.site.register(House, HouseConfig)
admin.site.register(Tenant, TenantConfig)
admin.site.register(Repair, RepairConfig)
admin.site.register(VisitRequest,VisitConfig)
admin.site.register(TenantRental,TenantRentalConfig)
admin.site.register(Library,LibraryConfig)
admin.site.register(Timeslot,TimeslotConfig)
admin.site.register(RentalInfo, RentalInfoConfig)