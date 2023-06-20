from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
import redis
from django.conf import settings
import json

from api.models.users import CustomUser

from backend import settings

GETMETHOD = 'GET'
POSTMETHOD = 'POST'
PUTMETHOD = 'PUT'
DELETEMETHOD = 'DELETE'


DEFAULTPASS = "wenhuashamo123."

# Set redis_client
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)

# get the user from redis
# @param:
#   -key: the sessionID from the front_end 
def get_user_from_redis(key):
    user_id = redis_client.get(key)
    if user_id is not None:
        user = CustomUser.objects.filter(id=user_id).first()
        if user:
            return user
    return None

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

# Centralized return format
def return_response(code, message, data = []):
    return UTF8JsonResponse({'errno': code, 'msg': message, 'data': data})

class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)