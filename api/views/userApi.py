from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from django.http import JsonResponse
from api.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from ..utils import *
from ..error_utils import *
import json

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return not_post_method()

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

    if not request.session.session_key:
        request.session.save() #保存之后生成session_key，之后前端以此为标头请求后端
    session_id = request.session.session_key

    # set session_id with user.id to redis
    redis_client.set(session_id, str(current_user.id), ex=12*60*60)


    print(f"Session ID: {request.session.session_key}")
    print(f"Session UID: {request.session.get('uid')}")

    data = {
        'username': current_user.username,
        'email': current_user.email,
        'phonenumber': current_user.contactNumber,
        'position': current_user.position,
        'realname': current_user.realname,
        'session_id': session_id,
        'userId': str(current_user.id),
        'valueInRedis': str(redis_client.get(session_id))
    }
    return return_response(100000, '登录成功', data)

# session_id
@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return not_post_method()

    session_id = json.loads(request.body)['session_id']
    session_value = redis_client.get(session_id)
    print(f"Before logout session_id: {session_id}")
    print(f"Before logout value session_id: {session_value}")

    if session_value is not None:
        redis_client.delete(session_id)
        return return_response(100000, '登出成功')
    return return_response(100001, '请先登录')


@csrf_exempt
def change_password(request):
    if request.method != 'POST':
        return not_post_method()

    session_id = request.POST.get('session_id')
    user = get_user_from_redis(session_id)
    if user is None:
        return no_user()

    try:
        info = request.POST.dict()
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
    except Exception as e:
        return default_error(e)

    user = CustomUser.objects.filter(id=uid, password=make_password(old_password,"a","pbkdf2_sha1")).first()
    if user:
        user.password = make_password(new_password,"a","pbkdf2_sha1")
        user.save()
        return return_response(100011, '修改密码成功')
    else:
        return return_response(100012, '密码错误')



