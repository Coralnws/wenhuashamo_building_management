from datetime import timedelta
from datetime import datetime
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils import timezone
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from ..utils import *
from api.search import *
from django.forms.models import model_to_dict


client = connections.create_connection(hosts=['http://120.46.205.87:9200'],
                                       http_auth=('elastic'), timeout=40)
paper_index = "title1"
author_index = "author"

def showScholarPage(request):
    #info = json.loads(request.body)
    d = request.GET.get('scholarId','')
    print(d)
    if d is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': 'search请求为空'},charset='utf-8')
    # d = {"name": "Ren Bao-Cang", "relative_paper_num": 20}
    # 返回作者
    author = Search(using=client, index=author_index)

    q = Q({"match": {"id" : d }})
    author = author.query(q)
    res_a = author.execute()

    # # 返回相关文献
    # paper = Search(using=client, index=paper_index).extra(from_=0, size=d["relative_paper_num"])

    # q = Q({"match_phrase": {"authors.name": "*" + d["name"] + "*"}})
    # paper = paper.query(q)
    # res_p = paper.execute()

    # ret = {"author": [hit.to_dict() for hit in res_a], "paper": [hit.to_dict() for hit in res_p]}
    # print(ret)
    ret = {"author": [hit.to_dict() for hit in res_a]}
    return UTF8JsonResponse({'errno': 100000, 'msg': '查询成功', 'post': ret})
            

    return UTF8JsonResponse({'errno':1001, 'msg': '返回学者信息','data':result})
        