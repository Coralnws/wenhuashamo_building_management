
from datetime import timedelta
from datetime import datetime,timedelta
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
from api.utils import *
from api.error_utils import *

"""
separate by year -> category by month -> recognize different type in each month
1.报修工作
    每年每月的每种维修类型工作数量
2.访客数量
    统计大厦访客数量，按照日期每天，每月统计，以及按照公司统计。
"""

@csrf_exempt
def repair_statistic(request):
    if request.method != GETMETHOD:
        return not_get_method()

    year = request.GET.get('year','')
    search_prefix = str(year)
    
    #filter every month
    return_data={}
    return_data['year'] = year #哪一年的数据
    return_data['water'] = 0 #按年的水维修数据
    return_data['electric'] = 0  #按年的电维修数据
    return_data['mechanic'] = 0  #按年的机械维修数据
    return_data['month'] = []


   
    record_list_data=[] #整体数据
    record_data=[]
    #整体数据里有多个record_data[],每个record_data[]代表一个月的数据，包括该月整体数量和各个种类维修工作
    #类型是看staff的type，如果staff.type[0]=='1'的话就是水

    for i in range(1,13):
        data={}
        data['month'] = str(i)
        data['water'] = 0
        data['electric'] = 0
        data['mechanic'] = 0
        data['other'] = 0

        if i < 10:
            time_prefix = search_prefix + "-0" + str(i)
        else:
            time_prefix = search_prefix + "-" + str(i)

        record_list = Repair.objects.filter(createdTime__startswith=time_prefix)
        for record in record_list:
            if record.staff and record.staff.m_type[0] == '1':
                data['water'] += 1;
            if record.staff and record.staff.m_type[1] == '1':
                data['electric'] += 1;
            if record.staff and record.staff.m_type[2] == '1':
                data['mechanic'] += 1;
            
            """
            if record.type == '1':
                data['water'] += 1;
            if record.type == '2':
                data['electric'] += 1;
            if record.type == '3':
                data['mechanic'] += 1;
            if record.type == '0':
                data['other'] += 1;
            """

        return_data['water'] += data['water']
        return_data['electric'] += data['electric']
        return_data['mechanic'] += data['mechanic']
            
        return_data['month'].append(data)  #统计完一个月的数据后把这个月append进整体的datas

    return UTF8JsonResponse({'errno':1001, 'msg': '成功获取报修列表','data':return_data})




"""
{
    "errno": 1001,
    "msg": "返回缴费记录成功",
    "data": [
        [
            {
                "year": "2022",
                "id": "cb444c7f-4b1f-4ced-a0d3-21ba3025aaae",
                "paymentTime": "2022-02-01T00:00:00",
                "amount": 1300
            }
        ],
        [],
        []
    ]
}
"""