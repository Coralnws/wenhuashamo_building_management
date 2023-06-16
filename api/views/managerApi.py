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

 #包括各个人姓名、电话、岗位。对于维修人员需要给出类型（水、电、机械）、是否可用状态。
 # listInfo - 0=管理人员 ,1=维修人员
 # managerManage : POST,PUT,DEL
 # servicemanManage : POST,PUT,DEL
 # searchStaff - 
