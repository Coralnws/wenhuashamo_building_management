
from api.error_utils import *
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from api.utils import *
from django.db.models import Q

def sendSms(request):
    phone = request.POST.get('phone')
    return phone_send(phone, 123123)


def phone_send(phone, code):
    # phone = "18805509919"  # 这里是测试用的，实际使用删除即可
    # 生成验证码.
    print("sending sms to :....", phone)
    
    # 短信验证
    client = AcsClient('LTAI5t8Rx7pvqC6VKvR74Tqd',
                       'bcRU4uXMHqusp8OR6e1QD8x0KQdmRp')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-beijing")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "buaa物业管理系统")
    request.add_query_param('TemplateCode', "SMS_461555205")

    request.add_query_param('TemplateParam', "{\"code\":\"%s\"}" % code)

    response = client.do_action_with_exception(request)  # 这里是阿里云官方接口的返回信息
    res = response.decode('utf-8')
    print("Reponse from ali:", response.decode('utf-8'))
    return return_response(100001, "sent sms", json.loads(res))
