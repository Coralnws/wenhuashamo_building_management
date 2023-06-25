
from api.error_utils import *
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from api.utils import *
from django.db.models import Q
from api.models import *
from api.scheduler.email_reminder import send_fee_reminder_smtp

def resend_otp(request):
    if request.method != 'POST':
        return not_post_method()
    
    info = request.POST.dict()
    visit_id = info.get('visit_id')

    visit = VisitRequest.objects.filter(id=visit_id).first()
    code = get_random_codes()
    res = phone_send(phone, code)
    if res.Code == 'OK':
        visit.otp = code
        v.otp_sent += 1
        v.save()

    return return_response(1001, "成功获取验证码")


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
    print("Reponse from ali:", res)
    return json.loads(res)



def get_random_codes():
    code = ''
    str1 = '0123456789'
    for i in range(0, 6):
        code += str1[random.randrange(0, len(str1))]
    return code