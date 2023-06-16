from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.forms import model_to_dict
from django.http import JsonResponse
from django.core.validators import validate_email
from api.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from ..utils import *


#r_session = django_redis.get_redis_connection(alias="session")

def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except:
        return False

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 100001, 'msg': '请求格式有误，不是POST'})
    info = request.POST.dict()
    username=info.get('username')
    email=info.get('email')
    password=info.get('password')
    securityQuestion=info.get('securityQuestion')
    securityAnswer=info.get('securityAnswer')
    if CustomUser.objects.filter(username=username).first():
        return UTF8JsonResponse({'errno': 100002, 'msg': '用户名已存在'})
    if not ValidateEmail(email):
        return UTF8JsonResponse({'errno': 100003, 'msg': '邮箱格式有误'})
    if CustomUser.objects.filter(email=email).first():
        return UTF8JsonResponse({'errno': 100004, 'msg': '邮箱已被注册'})
    if password != info.get('password2'):
        return UTF8JsonResponse({'errno': 100005, 'msg': '两次密码不一致'})
    del info['password2']
    CustomUser.objects.create_user(**info)

    return UTF8JsonResponse({'errno': 100000, 'msg': '注册成功'})


@csrf_exempt
def login(request):
    if request.session.get('uid'):
        return UTF8JsonResponse({'errno': 100004, 'msg': '已经登录，请勿重复登录'})
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 100001, 'msg': '请求格式有误，不是POST'})
    info = request.POST.dict()
    email = info.get('email')
    password = info.get('password')
    password = make_password(password, "a", "pbkdf2_sha1")

    currentUser = CustomUser.objects.filter(email=email).first()
    if currentUser is None:
        return UTF8JsonResponse({'errno': 100002, 'msg': '用户不存在或未注册'})

    if password != currentUser.password:
        return UTF8JsonResponse({'errno': 100003, 'msg': '邮箱或密码错误'})

    request.session['uid'] = str(currentUser.id)
    request.session.set_expiry(12*60*60)#12小时有效期
    if not request.session.session_key:
        request.session.save()#保存之后生成session_key，之后前端以此为标头请求后端
    session_id = request.session.session_key

    post = {
        'email': email,
        'username': currentUser.username,
        'real_name': currentUser.real_name,
        'session_id':session_id,
    }
    return UTF8JsonResponse({'errno': 100000, 'msg': '登录成功', 'post': post})

@csrf_exempt
def logout(request):
    if request.session.get('uid') is None:
        return UTF8JsonResponse({'errno': 100001, 'msg': '请先登录'})
    del request.session['uid']
    return UTF8JsonResponse({'errno': 100000, 'msg': '登出成功'})


@csrf_exempt
def updateInfo(request):
    info = request.POST.dict()
    real_name = info.get('real_name')  # 真名
    username=info.get('username')
    bio=info.get('bio')
    dob=info.get('dob')
    gender=info.get('gender')
    wbId=info.get('wbId')
    vxId=info.get('vxId')
    qqId=info.get('qqId')
    position=info.get('position')

    # email = info.get('email')
    # if email is None:
    #     return UTF8JsonResponse({'errno': 800001, 'msg': '邮箱不能为空'})
    uid=request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
    # if real_name is None and username is None:
    #     return UTF8JsonResponse({'errno': 800001, 'msg': '用于更新的真名和昵称至少要填入一项'})

    user = CustomUser.objects.filter(id=uid).first()
    if user is None:
        return UTF8JsonResponse({'errno': 800003, 'msg': '用户不存在'})
    try:
        if real_name:
            user.real_name=real_name
        if username:
            user.username=username
        if bio:
            user.bio=bio
        if dob:
            user.dob=dob
        if gender:
            user.gender=gender
        if wbId:
            user.wbId=wbId
        if qqId:
            user.qqId=qqId
        if vxId:
            user.vxId=vxId
        if position:
            user.position=position
        user.save()
    except Exception as e:
        return UTF8JsonResponse({'errno': 800004, 'msg': '数据库存储错误'+str(e.args)})
    return UTF8JsonResponse({'errno': 800000, 'msg': '修改成功'})


@csrf_exempt
def addThumbnail(request):
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 900002, 'msg': '请求格式有误，不是POST'})

    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    user = CustomUser.objects.filter(id=uid).first()
    if user is None:
        return UTF8JsonResponse({'errno': 900003, 'msg': '用户不存在'})

    try:
        thumbnail = request.FILES.get('thumbnail')
    except Exception as e:
        return UTF8JsonResponse({'errno': 900004, 'msg': '图片文件未正确上传'+str(e.args)})
    try:
        user.thumbnail.delete(save=False)  # 删除原头像
        user.thumbnail = thumbnail
        user.save()
    except Exception as e:
        return UTF8JsonResponse({'errno': 900005, 'msg': '头像保存失败'+str(e.args)})
    return UTF8JsonResponse({'errno': 900000, 'msg': '上传成功', 'thumbnail_url': user.get_thumbnail_url()})


#   获取头像在内的所有用户信息(不含敏感信息)
@csrf_exempt
def getUserMsg(request):
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
    user = CustomUser.objects.filter(id=uid).first()
    if user is None:
        return UTF8JsonResponse({'errno': 900013, 'msg': '用户不存在'})
    try:
        dict1 = model_to_dict(user)
        del dict1['thumbnail']
        del dict1['profile']
        dict1['thumbnail_url'] = user.get_thumbnail_url()
    except Exception as e:
        return UTF8JsonResponse({'errno': 800004, 'msg': '数据库存储错误'+str(e.args)})
    return UTF8JsonResponse({'errno': 900010, 'msg': '获取成功', 'backend_data': dict1})


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


@csrf_exempt
def sendMessage(request):
    import random
    email = request.POST.get('email')
    if ValidateEmail(email):
        str1 = '0123456789'
        rand_str = ''
        for i in range(0, 6):
            rand_str += str1[random.randrange(0, len(str1))]
        # 发送邮件：
        # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
        message = "您的验证码是" + rand_str + "，10分钟内有效，请尽快填写"
        emailBox = []
        emailBox.append(email)
        send_mail('墨书验证码', message, 'moshu_inkbook@163.com', emailBox, fail_silently=False)
        #    return rand_str
        return UTF8JsonResponse({'errno': 100000, 'msg': '成功发送', 'str': rand_str})
    else:
        return UTF8JsonResponse({'errno': 100001, 'msg': '邮箱不正确'})

@csrf_exempt
def forgotPassword(request):
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 800002, 'msg': '请求格式有误，不是POST'})
    question=request.POST.get('question')
    answer=request.POST.get('answer')
    email=request.POST.get('email')
    
    if ValidateEmail(email):
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return UTF8JsonResponse({'errno': 900024, 'msg': '该邮箱不存在'})
        print(user.securityQuestion==question)
        if user.securityQuestion==question and user.securityAnswer==answer:
            password=request.POST.get('password')
            password2=request.POST.get('password2')
            if password == password2:
                user.password = make_password(password,"a","pbkdf2_sha1")
                user.save()
                return UTF8JsonResponse({'errno': 900020, 'msg': '修改密码成功'})
            else:
                return UTF8JsonResponse({'errno': 900021, 'msg': '两个密码不一致'})
        else:
            return UTF8JsonResponse({'errno': 900022, 'msg': '密保问题与答案不正确'})
    else:
        return UTF8JsonResponse({'errno': 900023, 'msg': '邮箱格式不正确'})
    
@csrf_exempt
def getQuestion(request):
    if request.method != 'POST':
        return UTF8JsonResponse({'errno': 800002, 'msg': '请求格式有误，不是POST'})
    email=request.POST.get('email')
    user = CustomUser.objects.filter(email=email).first()
    print("hi")
    if user is None:
        return UTF8JsonResponse({'errno': 900024, 'msg': '该邮箱不存在'})
    else:
        data={}
        data['question']=user.securityQuestion
        return UTF8JsonResponse({'errno': 900020, 'msg': '返回密保问题','data':data})

