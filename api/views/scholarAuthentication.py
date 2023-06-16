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

@csrf_exempt
def requestScholarAuthenticate(request):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    # check login user really existed
    user = get_auth_user(uid)
    info = request.POST.dict()
    scholarId = info.get('scholarId')

    if user is None:
        return UTF8JsonResponse({'errno': 3001, 'msg': "用户不存在"})

    if user.scholarAuth is not None:
        return UTF8JsonResponse({'errno': 3005, 'msg': "用户已有学者门户"})

    # find scholar to see if found or not
    # get the scholar info from ES
    try:
        scholar = searchAuthor(scholarId)['results'][0][0]
    except:
        scholar = None

    if scholar is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4002, 'msg': "学者不存在"})

    userAuthScholar = UserAuthenticateScholar.objects.filter(scholar_id=scholarId).first()

    if userAuthScholar is not None:
        return UTF8JsonResponse({'errno': 3003, 'msg': "学者已被认领"})

    anotherUserAuthScholar = UserAuthenticateScholar.objects.filter(user_id=user.id).first()

    if anotherUserAuthScholar is not None:
        return UTF8JsonResponse({'errno': 3010, 'msg': "该用户已有学者"})

    scholar_name = scholar['name'].replace(" ", "")

    match = False
    names = user.real_name.split(' ')
    for name in names:
        if name in scholar_name:
            match = True

    if not match:
        return UTF8JsonResponse({'errno': 3002, 'msg': "用户名与学者名不符"})
        
    genCode = gen_code()
    oldCode = Code.objects.filter(sendTo=user).first()
    if oldCode:
        oldCode.code = genCode
        oldCode.updatedAt = timezone.now()
        oldCode.save()
    else:
        code = Code()
        code.code = genCode
        code.sendTo = user
        code.save()
    send_smtp(user,scholar,request,genCode,"Scholar Authentication 认领学者身份","authenticate_scholar.txt")
    return UTF8JsonResponse({'errno': 1001, 'msg': "邮件已发送"})


@csrf_exempt
def validateScholarAuthenticate(request):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    # Check whether login user really exists
    user = get_auth_user(uid)
    if user is None:
        return UTF8JsonResponse({'errno': 3001, 'msg': "用户不存在"})

    if user.scholarAuth is not None:
        return UTF8JsonResponse({'errno': 3005, 'msg': "用户已有学者门户"})

    info = request.POST.dict()
    code = info.get('code')
    scholarId = info.get('scholarId')

    # find scholar to see if found or not
    # todo need to use ES to find the scholar and update the scholar
    # scholar = Scholar.objects.filter(id=scholarId).first()
    # get the scholar info from ES
    try:
        scholar = searchAuthor(scholarId)['results'][0][0]
    except:
        scholar = None

    if scholar is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4002, 'msg': "学者不存在"})

    userAuthScholar = UserAuthenticateScholar.objects.filter(scholar_id=scholarId).first()

    if userAuthScholar is not None:
        return UTF8JsonResponse({'errno': 3003, 'msg': "学者已被认领"})

    anotherUserAuthScholar = UserAuthenticateScholar.objects.filter(user_id=user.id).first()

    if anotherUserAuthScholar is not None:
        return UTF8JsonResponse({'errno': 3010, 'msg': "该用户已有学者"})

    oldCode = Code.objects.filter(sendTo=user).first()
    if oldCode is None:
        return UTF8JsonResponse({'errno': 3005, 'msg': "用户没有申请学者认证"})

    if code != oldCode.code:
        return UTF8JsonResponse({'errno': 3004, 'msg': "验证码不正确"})

    if timezone.now() > oldCode.updatedAt + timedelta(minutes=15):
        return UTF8JsonResponse({'errno': 3003, 'msg': "验证码已过期"})

    user.scholarAuth = scholarId
    user.save()

    newUserAuth = UserAuthenticateScholar()
    newUserAuth.scholar_id = scholarId
    newUserAuth.user_id = user.id
    newUserAuth.save()

    oldCode.delete()
    return UTF8JsonResponse({'errno': 1002, 'msg': "认领学者成功"})