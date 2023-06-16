from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random

from api.models.users import CustomUser

from backend import settings

#send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt", True)
def send_smtp(user,scholar,request,code,subject, fileName):
    context = {
        'username': user.username,
        'scholar' : scholar["name"],
        'code' : code,
        'email': user.email
    }
    print(settings.EMAIL_FROM_USER)
    email = EmailMessage(
        subject,
        render_to_string(fileName, context),
        settings.EMAIL_FROM_USER, # FROM
        [user.email],    #TO
    )

    email.send(fail_silently=False)
    #return UTF8JsonResponse({'errno': 1001, 'msg': "邮件已发送"})

def send_article_smtp(user,article,request,code,subject, fileName):
    context = {
        'username': user.username,
        'article' : article['title'],
        'code' : code,
        'email': user.email
    }
    print(settings.EMAIL_FROM_USER)
    email = EmailMessage(
        subject,
        render_to_string(fileName, context),
        settings.EMAIL_FROM_USER, # FROM
        [user.email],    #TO
    )

    email.send(fail_silently=False)
    #return UTF8JsonResponse({'errno': 1001, 'msg': "邮件已发送"})

def gen_code(length=6):
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
        print(rand_str)
    return rand_str

def get_auth_user(uid):
    user = CustomUser.objects.filter(id=uid).first()
    if user:
        return user
    return None

class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)