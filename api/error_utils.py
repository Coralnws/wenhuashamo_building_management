from .utils import *

def not_post_method():
    return return_response(400001, "格式错误，不是 POST 请求！")

def not_get_method():
    return return_response(400001, "格式错误，不是 GET 请求！")

def not_put_method():
    return return_response(400001, "格式错误，不是 PUT 请求！")

def not_delete_method():
    return return_response(400001, "格式错误，不是 DELETE 请求！")

def no_user():
    return return_response(400002, "用户不存在")

def not_login():
    return return_response(400002, "用户没登录")

def default_error(e):
    return return_response(99999, "请求数据字段错误" + str(e.args))