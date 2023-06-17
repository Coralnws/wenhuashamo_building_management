from datetime import timedelta
from datetime import datetime
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from ..utils import *
from django.forms.models import model_to_dict
from django.db.models import Q
import operator

''' 增删改查
从合同签约日期开始，按年给出是否缴纳物业费，以及缴费具体时间
物业费每年缴纳1次，从签约开始（例如计算每个月多少钱）

增：
增加缴费记录
1. createPaymentRecord : (未确定要通过 tenant/rentalInfo/house 定位)
    拿到Id后,添加的是payment,所以要拿到payment的属性value
删：
1. delPaymentRecord

改：
改缴费记录 or 改缴费状态
1. updatePaymentRecord - 比较常见是改缴费时间
2. updatePayStatus - 修改缴费状态，应该要给出缴费记录的修改，改成什么状态都需要给出下一个缴费截止时间
                     （改成未缴费就把deadline减回上一个周期 、改成已缴费就变成下一个周期）
查：
1. getTenantRecord - 单人记录，查看Tenant一直以来的缴费记录（物业费+租赁费，get的时候分类分开）
                      这边list的时候注意看可不可以按年给出， 写这边有没有缴费，有的话就list出记录，没有就False2
2. getUnpaidRecord - 列出目前欠物业费/租赁费的人,这边后面可以加个search功能
                     通过rentalInfo找，返回House+Tenant信息
3. getHouseRecord - 房屋记录，查看某房一直以来的缴费记录（物业费+租赁费，get的时候分类分开）
'''

@csrf_exempt
def createRecord(request):
    if request.method == 'POST':
        info = request.POST.dict()
        tenantId = info.get('tenantId') #针对租客
        houseId = info.get('houseId')  #针对房屋
        rentalInfoId = info.get('rentalId')  #针对租赁合约

        type = info.get('paymentType')
        t


'''
    TYPE = (
        ('0','暂无'),
        ('1','租赁费'),
        ('2','物业费'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE, null=False, blank=False)
    createdTime = models.DateTimeField(default=timezone.now)
    rentalInfo = models.ForeignKey("RentalInfo", on_delete=models.CASCADE, null=False, blank=False)
    amount = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE,default='0')
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
''' 

        

        