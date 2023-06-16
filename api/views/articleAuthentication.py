from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.utils import timezone
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from ..utils import *
from api.search import *

@csrf_exempt
def requestArticleAuthenticate(request):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    # check login user really existed
    user = get_auth_user(uid)
    info = request.POST.dict()
    articleId = info.get('articleId')

    if user is None:
        return UTF8JsonResponse({'errno': 3001, 'msg': "用户不存在"})

    userAuthScholar = UserAuthenticateScholar.objects.filter(user_id=user.id).first()

    if user.scholarAuth is None or userAuthScholar is None:
        return UTF8JsonResponse({'errno': 3010, 'msg': "该用户没有认领过学者，不能认领学术成果，请先认领学者门户"})

    # find article to see if found or not
    # article = Article.objects.filter(id=articleId).first()
    try:
        article = searchPaper(articleId)['results'][0][0]
    except:
        article = None

    if article is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4001, 'msg': "学术成果不存在"})

    scholarsInArticle = [author["id"] for author in article['authors']]

    if userAuthScholar.scholar_id in scholarsInArticle:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4015, 'msg': "该学者已经是该学术成果的作者，不能再认领"})

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
    send_article_smtp(user, article, request, genCode, "Article Authentication 认领学术成果", "authenticate_article.txt")
    return UTF8JsonResponse({'errno': 1001, 'msg': "邮件已发送"})


@csrf_exempt
def validateArticleAuthenticate(request):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    # Check whether login user really exists
    user = get_auth_user(uid)
    if user is None:
        return UTF8JsonResponse({'errno': 3001, 'msg': "用户不存在"})

    info = request.POST.dict()
    code = info.get('code')
    articleId = info.get('articleId')

    userAuthScholar = UserAuthenticateScholar.objects.filter(user_id=user.id).first()

    if user.scholarAuth is None or userAuthScholar is None:
        return UTF8JsonResponse({'errno': 3010, 'msg': "该用户没有认领过学者，不能认领学术成果，请先认领学者门户"})

    # find article to see if found or not
    # article = Article.objects.filter(id=articleId).first()
    try:
        article = searchPaper(articleId)['results'][0][0]
    except:
        article = None

    if article is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4001, 'msg': "学术成果不存在"})

    scholarsInArticle = [author["id"] for author in article['authors']]

    if userAuthScholar.scholar_id in scholarsInArticle:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4015, 'msg': "该学者已经是该学术成果的作者，不能再认领"})

    oldCode = Code.objects.filter(sendTo=user).first()
    if oldCode is None:
        return UTF8JsonResponse({'errno': 3005, 'msg': "用户没有申请学者认证"})

    if code != oldCode.code:
        return UTF8JsonResponse({'errno': 3004, 'msg': "验证码不正确"})

    if timezone.now() > oldCode.updatedAt + timedelta(minutes=15):
        return UTF8JsonResponse({'errno': 3003, 'msg': "验证码已过期"})

    #todo update the authors fields in paper using ES

    newArticleAuthRecord = UserAuthenticateArticle()
    newArticleAuthRecord.user_id = user.id
    newArticleAuthRecord.article_id = article['id']
    newArticleAuthRecord.save()

    return UTF8JsonResponse({'errno': 1002, 'msg': "认领学术成果成功"})