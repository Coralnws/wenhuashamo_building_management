from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from django.http import JsonResponse
from api.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from ..utils import *
import json

@csrf_exempt
def login(request):
    # if request.session.get('uid'):
        # return UTF8JsonResponse({'errno': 100004, 'msg': '已经登录，请勿重复登录'})
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 100001, 'msg': '请求格式有误，不是POST'})
    info = json.loads(request.body)

    username = info['username']
    password = info['password']
    password = make_password(password, "a", "pbkdf2_sha1")

    current_user = CustomUser.objects.filter(username=username).first()
    current_email_user = CustomUser.objects.filter(email=username).first()
    current_phone_user = CustomUser.objects.filter(contactNumber=username).first()

    if current_user is None and current_email_user is None and current_phone_user is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': '用户不存在'})

    if password != current_user.password:
        return UTF8JsonResponse({'errno': 100003, 'msg': '密码错误'})

    request.session['uid'] = str(current_user.id)
    request.session.set_expiry(12*60*60)#12小时有效期


    if not request.session.session_key:
        request.session.save() #保存之后生成session_key，之后前端以此为标头请求后端
    session_id = request.session.session_key

    print(f"Session ID: {request.session.session_key}")
    print(f"Session UID: {request.session.get('uid')}")

    data = {
        'username': current_user.username,
        'email': current_user.email,
        'phonenumber': current_user.contactNumber,
        'position': current_user.position,
        'realname': current_user.realname,
        'session_id':session_id,
        'userId':current_user.id,
        'requestuid': request.session.get('uid'),
    }
    return UTF8JsonResponse({'errno': 100000, 'msg': '登录成功', 'data': data})

@csrf_exempt
def logout(request):
    print(f"in House Inspect Session ID: {request.session.session_key}")
    print(f"In House Inspect before logout: {request.session.get('uid')}")
    if request.session.get('uid') is None:
        return UTF8JsonResponse({'errno': 100001, 'msg': '请先登录'})
    del request.session['uid']
    print(f"Session UID after logout: {request.session.get('uid')}")
    return UTF8JsonResponse({'errno': 100000, 'msg': '登出成功'})


@csrf_exempt
def changePassword(request):
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
    try:
        info = request.POST.dict()
        old_password = info.get('old_password')
        new_password = info.get('new_password')
    except Exception as e:
        return UTF8JsonResponse({'errno': 800004, 'msg': '请求数据字段错误'+str(e.args)})

    user = CustomUser.objects.filter(id=uid, password=make_password(old_password,"a","pbkdf2_sha1")).first()
    if user:
        user.password = make_password(new_password,"a","pbkdf2_sha1")
        user.save()
        return UTF8JsonResponse({'errno': 900020, 'msg': '修改密码成功'})
    else:
        return UTF8JsonResponse({'errno': 900021, 'msg': '密码错误'})



