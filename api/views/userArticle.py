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

@csrf_exempt
def bookmarkArticle(request):
    if request.method == 'POST':
        # userId=request.session.get('uid')
        # if userId is None:
        #     return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        userId=request.POST.get('userId')
        paperId=request.POST.get('paperId')
        paperName = request.POST.get('paperName')
        user=CustomUser.objects.filter(id=userId).first()
    
        existRecord=UserArticle.objects.filter(user=user,article=paperId).first()
        if existRecord:
            if existRecord.isBookmark == True:
                existRecord.isBookmark=False
                existRecord.save()
                data=model_to_dict(existRecord)
                return UTF8JsonResponse({'errno':1001, 'msg': '成功取消收藏','userArticle':data})
            else:
                existRecord.isBookmark=True
                existRecord.save()
                data=model_to_dict(existRecord)
                return UTF8JsonResponse({'errno':1001, 'msg': '成功收藏学术成果','userArticle':data})
        else:
            userArticle = UserArticle(user=user,article=paperId,articleName=paperName,isBookmark=True)
            userArticle.save()

            data=model_to_dict(userArticle)

            return UTF8JsonResponse({'errno':1001, 'msg': '成功收藏学术成果','userArticle':data})

@csrf_exempt
def createHistory(request):
    if request.method == 'POST':
        userId=request.session.get('uid')
        if userId is None:
            return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        # userId=request.POST.get('userId')
        paperId=request.POST.get('paperId')
        paperName = request.POST.get('paperName')
        user=CustomUser.objects.filter(id=userId).first()
    
        history = History(belongTo=user,article=paperId,articleName=paperName)
        history.save()
        
        data=model_to_dict(history)
        return UTF8JsonResponse({'errno':1001, 'msg': '成功创建浏览记录','history':data})

@csrf_exempt
def getBookmarkList(request):
    if request.method == 'GET':
        userId=request.session.get('uid')
        if userId is None:
            return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        #userId=request.GET.get('userId')
        user=CustomUser.objects.filter(id=userId).first()
        bookmarkList=UserArticle.objects.filter(user=user,isBookmark=True)

        data = []
        for tmp in bookmarkList:
            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            data.append(data1)
            
        return UTF8JsonResponse({'errno':1001, 'msg': '返回收藏列表成功', 'data': data})

@csrf_exempt
def getHistoryList(request):
    if request.method == 'GET':
        userId=request.session.get('uid')
        if userId is None:
            return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        #userId=request.GET.get('userId')
        user=CustomUser.objects.filter(id=userId).first()
        historyList=History.objects.filter(belongTo=user).order_by('-createdAt')

        data = []
        for tmp in historyList:
            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            data.append(data1)
            
        return UTF8JsonResponse({'errno':1001, 'msg': '返回浏览记录成功', 'data': data})