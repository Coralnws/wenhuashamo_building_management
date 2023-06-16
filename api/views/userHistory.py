from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import *


@csrf_exempt
def addHistory(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 800001, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return JsonResponse({'errno': 800000, 'msg': '当前cookie为空，未登录，请先登录'})
    user = CustomUser.objects.filter(id=uid).first()
    info = request.POST.dict()
    articleId = info.get('articleId')
    article = Article.objects.filter(id=articleId).first()
    newHistory = History()
    newHistory.article = article
    newHistory.belongTo = user
    newHistory.save()
    return JsonResponse({'status': 1, 'errno': 800003, 'msg': "成功保存"})

@csrf_exempt
def viewHistory(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 800001, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return JsonResponse({'errno': 800000, 'msg': '当前cookie为空，未登录，请先登录'})
    user = CustomUser.objects.filter(id=uid).first()
    historyList = History.objects.filter(belongTo=user)
    data = []
    for x in historyList:
        data.append(x.article.id)

    return JsonResponse({'errno': 800002, 'msg': '返回浏览记录成功', 'data': data})
