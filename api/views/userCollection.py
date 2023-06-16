from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from django.forms.models import model_to_dict

from api.models.collection import Collection


@csrf_exempt
def addCollection(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 800001, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return JsonResponse({'errno': 800000, 'msg': '当前cookie为空，未登录，请先登录'})
    user = CustomUser.objects.filter(id=uid).first()
    info = request.POST.dict()
    articleId = info.get('articleId')
    article = Article.objects.filter(id=articleId).first()
    newCollection = Collection()
    newCollection.article = article
    newCollection.belongTo = user
    newCollection.save()
    return JsonResponse({'status': 1, 'errno': 800003, 'msg': "成功收藏"})

@csrf_exempt
def viewCollection(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 800001, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return JsonResponse({'errno': 800000, 'msg': '当前cookie为空，未登录，请先登录'})
    user = CustomUser.objects.filter(id=uid).first()
    collectionList = Collection.objects.filter(belongTo=user)
    data = []
    for x in collectionList:
        data.append(x.article.id)

    return JsonResponse({'errno': 800002, 'msg': '返回收藏记录成功', 'data': data})

@csrf_exempt
def cancelCollection(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 800001, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return JsonResponse({'errno': 800000, 'msg': '当前cookie为空，未登录，请先登录'})
    user = CustomUser.objects.filter(id=uid).first()
    info = request.POST.dict()
    articleId = info.get('articleId')
    article = Article.objects.filter(id=articleId).first()
    newCollection = Collection().objects.filter(article=article).delete()
    return JsonResponse({'status': 1, 'errno': 800004, 'msg': "成功删除"})
