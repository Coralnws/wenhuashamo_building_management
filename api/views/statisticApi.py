
import calendar
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
month_day_list = {'1': 31, '2': 28,'3':31,'4':30,'5':31,'6':30,
            '7':31,'8':31,'9':30,'10':31,'11':30,'12':31}


def month_day(year, month):
    return calendar.monthrange(year, month)[1]


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

        data['other'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=0).count()
        data['water'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=1).count()
        data['electric'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=2).count()
        data['mechanic'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=3).count()


        return_data['water'] += data['water']
        return_data['electric'] += data['electric']
        return_data['mechanic'] += data['mechanic']
            
        return_data['month'].append(data)  #统计完一个月的数据后把这个月append进整体的data

    return UTF8JsonResponse({'errno':1001, 'msg': '成功获取报修工作统计数据','data':return_data})

@csrf_exempt
def repair_statistic_year(request):
    if request.method != GETMETHOD:
        return not_get_method()

    start_year = request.GET.get('start_year','')
    end_year = request.GET.get('end_year','')
    
    time_prefix = start_year
    
    return_data=[]

    for year in range(int(start_year),int(end_year)+1):
        data={}
        data['year'] = year
        data['water'] = 0
        data['electric'] = 0
        data['mechanic'] = 0
        data['other'] = 0

        time_prefix = str(year)

        data['other'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=0).count()
        data['water'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=1).count()
        data['electric'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=2).count()
        data['mechanic'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=3).count()


        return_data.append(data)

    return UTF8JsonResponse({'errno':1001, 'msg': '成功获取报修工作统计数据','data':return_data})


"""
访客数量：每天和每月数据
"""
#暂时没用
@csrf_exempt
def visit_statistic(request):
    if request.method != GETMETHOD:
        return not_get_method()
    
    year = request.GET.get('year','')
    return_data=[]  #一年的数据

    for i in range(1,13):
        data = {} #每个月的数据
        data['month'] = i

        begin = datetime.date(year,i,1)
        end = datetime.date(year,i,month_day(2023,str(i)))
        for i in range((end - begin).days+1):
            day = begin + datetime.timedelta(days=i)
            num = VisitRequest.objects.filter(visit_time__startswith=day).count()
            data[str(day)] = num
            
        return_data.append(data)    
    return UTF8JsonResponse({'errno':1001, 'msg': '成功获取访客数量统计数据','data':return_data})

@csrf_exempt
def visit_statistic_month(request):
    if request.method != GETMETHOD:
        return not_get_method()
    
    year = request.GET.get('year','')
    month = request.GET.get('month','') or None
    data = {}
    data['company_data'] = []
    data['company_count'] = []
    data['day_data'] = []

    tmp_company_data = {}

    #计算某月的每一天数据
    time_prefix = None
    if int(month) < 10:
        time_prefix = year + "-0" + month
    else:
        time_prefix = year + "-" + month

    #筛出这个月的数据
    month_data_list = VisitRequest.objects.filter(visit_time__startswith=time_prefix).order_by('visit_time')

    begin = datetime.date(int(year),int(month),1)
    end = datetime.date(int(year),int(month),month_day(int(year),int(month)))

    for i in range((end - begin).days+1):
        day = begin + datetime.timedelta(days=i)
        num = month_data_list.filter(visit_time__startswith=day).count()
        if num != 0 :
            data['day_data'].append(num)
        else:
            data['day_data'].append(0)
    
    #对这个月的数据，去看有哪一天的数据，有哪间公司的数据
    for month_data in month_data_list:
        if tmp_company_data.get(month_data.company) is None:
           tmp_company_data[month_data.company] = 0
        tmp_company_data[month_data.company] += 1

    for key, value in tmp_company_data.items():
        data['company_data'].append(key)
        data['company_count'].append(value)

    return UTF8JsonResponse({'errno':1001, 'msg': '成功获取访客数量统计数据','data':data})




