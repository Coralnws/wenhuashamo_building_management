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

    current_user = (
        CustomUser.objects.filter(username=username).first() or
        CustomUser.objects.filter(email=username).first() or
        CustomUser.objects.filter(contactNumber=username).first()
    )

    if current_user is None:
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
    
    company=None
    company_contact_name=None
    company_contact_number=None
    if current_user.tenant:
        company = current_user.tenant.company
        company_contact_name = current_user.tenant.contactName
        company_contact_number = current_user.tenant.contactNumber


    data = {
        'is_change_password': current_user.is_change_password,
        'username': current_user.username,
        'email': current_user.email,
        'phonenumber': current_user.contactNumber,
        'position': current_user.position,
        'realname': current_user.realname,
        'session_id': session_id,
        'userId': str(current_user.id),
        'company':company,
        'company_contact_name' : company_contact_name,
        'company_contact_number' : company_contact_number,
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

    try:
        info = request.POST.dict()
        user_id = info.get('user_id')
        old_password = info.get('old_password')
        new_password1 = info.get('new_password1')
        new_password2 = info.get('new_password2')
    except Exception as e:
        return default_error(e)

    if new_password1 != new_password2:
        return return_response(100013, '新密码不同')


    user = CustomUser.objects.filter(id=user_id, password=make_password(old_password,"a","pbkdf2_sha1")).first()
    if user:
        user.password = make_password(new_password1,"a","pbkdf2_sha1")
        user.is_change_password = 1
        user.save()
        return return_response(100011, '修改密码成功')
    else:
        return return_response(100012, '密码错误')



