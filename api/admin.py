from django.contrib import admin
from .models import *

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username', 'realname','email', 'profile')

class PaymentConfig(admin.ModelAdmin):
    list_display = ('id', 'tenant')

class TenantConfig(admin.ModelAdmin):
    list_display = ('id', 'username','real_name')

class RepairConfig(admin.ModelAdmin):
    list_display = ('id', 'createdTime','house','company','contactName','contactNumber','staff',
                    'staffContact','manager','repairingTime','status','plan','completeTime','solver')

class HouseConfig(admin.ModelAdmin):
    list_display = ('id', 'roomNumber', 'floor')

class RentalInfoConfig(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'house','startTime', 'endTime','nextRentalDeadline','nextManagementFeeDeadline')


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Payment, PaymentConfig)
admin.site.register(House, HouseConfig)
admin.site.register(Tenant, TenantConfig)
admin.site.register(RentalInfo, RentalInfoConfig)