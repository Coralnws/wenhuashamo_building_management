
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

def month_day(year,month):
    if month == '2' and year % 4 == 0:
        return 29
    
    return month_day_list[month]


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

        # 之后替换这部分
        record_list = Repair.objects.filter(createdTime__startswith=time_prefix)
        for record in record_list:
            if record.staff and record.staff.m_type[0] == '1':
                data['water'] += 1;
            if record.staff and record.staff.m_type[1] == '1':
                data['electric'] += 1;
            if record.staff and record.staff.m_type[2] == '1':
                data['mechanic'] += 1;
        
        """  维修工单增加类型属性后 
        data['other'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=0).count()
        data['water'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=1).count()
        data['electric'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=2).count()
        data['mechanic'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=3).count()
        """

        return_data['water'] += data['water']
        return_data['electric'] += data['electric']
        return_data['mechanic'] += data['mechanic']
            
        return_data['month'].append(data)  #统计完一个月的数据后把这个月append进整体的datas

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
        #year = str(int(year)+1)
        data['water'] = 0
        data['electric'] = 0
        data['mechanic'] = 0
        data['other'] = 0

        time_prefix = str(year)

        record_list = Repair.objects.filter(createdTime__startswith=time_prefix)
        for record in record_list:
            if record.staff and record.staff.m_type[0] == '1':
                data['water'] += 1;
            if record.staff and record.staff.m_type[1] == '1':
                data['electric'] += 1;
            if record.staff and record.staff.m_type[2] == '1':
                data['mechanic'] += 1;

        """  维修工单增加类型属性后 
        data['other'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=0).count()
        data['water'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=1).count()
        data['electric'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=2).count()
        data['mechanic'] = Repair.objects.filter(createdTime__startswith=time_prefix,type=3).count()
        """

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
    return_data={} 
    data = {} 
    company_data = {}

    # begin = datetime.date(int(year),int(month),1)
    # end = datetime.date(int(year),int(month),month_day(2023,month))

    # 一年里每个月的访客数量
    if month is None:
        #先筛选出某一年
        year_data_list = VisitRequest.objects.filter(visit_time__startswith=year)

        #对那一年的每一个月去统计公司的数量
        for i in range(1,13):

            time_prefix = None
            if i < 10:
                time_prefix = year + "-0" + str(i)
            else:
                time_prefix = year + "-" + str(i)
            
            #这年的其中一月的数据
            month_data_list = year_data_list.filter(visit_time__startswith=time_prefix)

            #统计各个公司的数据
            for month_data in month_data_list:
                if company_data.get(month_data.company) is None:
                    company_data[month_data.company] = 0
                company_data[month_data.company] += 1

            #直接统计数量
            data[str(i)] = len(month_data_list)

        return_data['company_data'] = company_data
        return_data['month_data'] = data

        return UTF8JsonResponse({'errno':1001, 'msg': '成功获取访客数量统计数据','data':return_data})

    #计算某月的每一天数据
    time_prefix = None
    if int(month) < 10:
        time_prefix = year + "-0" + month
    else:
        time_prefix = year + "-" + month

    #筛出这个月的数据
    month_data_list = VisitRequest.objects.filter(visit_time__startswith=time_prefix).order_by('visit_time')
    """
    for i in range((end - begin).days+1):
        day = begin + datetime.timedelta(days=i)
        #num = month_data_list.filter(visit_time__startswith=day).count()
        data[str(day)] = 0
    """
    #对这个月的数据，去看有哪一天的数据，有哪间公司的数据
    for month_data in month_data_list:
        if data.get(str(month_data.visit_time.strftime("%Y-%m-%d"))) is None:
            data[str(month_data.visit_time.strftime("%Y-%m-%d"))] = 0
        if company_data.get(month_data.company) is None:
            company_data[month_data.company] = 0
        company_data[month_data.company] += 1
        data[str(month_data.visit_time.strftime("%Y-%m-%d"))] += 1

    return_data['company_data'] = company_data
    return_data['day_data'] = data
    
    return UTF8JsonResponse({'errno':1001, 'msg': '成功获取访客数量统计数据','data':return_data})




