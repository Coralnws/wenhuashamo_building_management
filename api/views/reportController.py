from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from ..utils import *
from api.search import *

@csrf_exempt
def reportScholar(request):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    info = request.POST.dict()
    user = get_auth_user(uid)
    title = info.get('title')
    description = info.get('description')
    createdBy = user
    scholarId = info.get('scholarId')

    # scholar = Scholar.objects.filter(id=scholarId).first()
    # get the scholar info from ES
    try:
        scholar = searchAuthor(scholarId)['results'][0][0]
    except:
        scholar = None

    if scholar is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4002, 'msg': "学者不存在"})

    userAuthScholar = UserAuthenticateScholar.objects.filter(scholar_id=scholar["id"]).first()

    if userAuthScholar is None:
        return UTF8JsonResponse({'errno': 4013, 'msg': "该学者门户还没认领，可以认领，不用申诉"})

    if userAuthScholar.user_id == user.id and userAuthScholar.scholar == scholar['id']:
        return UTF8JsonResponse({'errno': 4014, 'msg': "该用户已经申诉过该学者门户"})

    if user.scholarAuth is not None:
        return UTF8JsonResponse({'errno': 4011, 'msg': "用户已有学者门户，不能再申诉"})

    newReport = Report()
    newReport.title = title
    newReport.description = description
    newReport.reportScholar_id = scholar["id"]
    newReport.reportArticle_id = None
    newReport.category = 1 # 1 is for scholar
    newReport.result = 0    # 0 is for pending
    newReport.createdBy = createdBy
    newReport.save()

    # Notification
    noticeToUser = Notification(type=2, belongTo=user, scholarId=scholar["id"], scholarName=scholar["name"])
    noticeToUser.save()
    return UTF8JsonResponse(data={'status': 1, 'report': model_to_dict(newReport),'errno': 4003, 'msg': "成功发送申诉学者记录"})


@csrf_exempt
def reportArticle(request):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    info = request.POST.dict()
    user = get_auth_user(uid)
    title = info.get('title')
    description = info.get('description')
    createdBy = user
    articleId = info.get('paperId')
    scholarId = info.get('scholarId')

    try:
        article = searchPaper(articleId)['results'][0][0]
    except:
        article = None

    if article is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4001, 'msg': "学术成果不存在"})

    # get the scholar info from ES
    try:
        scholar = searchAuthor(scholarId)['results'][0][0]
    except:
        scholar = None

    if scholar is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4002, 'msg': "学者不存在"})

    # find whether the reported Scholar is in the article
    scholarsInArticle = [author["id"] for author in article['authors']]

    if scholar['id'] not in scholarsInArticle:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4015, 'msg': "该学者并不是该学术成果的作者"})

    newReport = Report()
    newReport.title = title
    newReport.description = description
    newReport.reportScholar_id = scholar.id
    newReport.reportArticle_id = article.id
    newReport.category = 2  # 2 is for Article report
    newReport.result = 0    # 0 is pending
    newReport.createdBy = createdBy
    newReport.save()

    noticeToUser = Notification(type=7, belongTo=user, paper=article['id'], scholarName=scholar['name'])
    noticeToUser.save()
    return UTF8JsonResponse(data={'status': 1, 'report': model_to_dict(newReport),'errno': 4003, 'msg': "成功发送申诉记录"})


@csrf_exempt
def rejectReport(request, reportId):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
    user = get_auth_user(uid)
    if user is None or not user.is_staff:
        return UTF8JsonResponse(data={'errno': 4010, 'msg': '不是管理员，不能操作'})

    report = Report.objects.filter(id=reportId).first()

    if report is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4004, 'msg': "申诉记录不存在"})
    if report.result != 0:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4005, 'msg': "无法修改申诉记录，因为其已经是在接受或者拒绝状态"})

    # get the scholar info from ES
    try:
        scholar = searchAuthor(report.reportScholar_id)['results'][0][0]
    except:
        scholar = None

    # when it is rejecting scholar
    if report.category == 1:
        newNotice = Notification(type=6, belongTo=user, scholarId=scholar['id'], scholarName=scholar['name'])
        newNotice.save()
        report.result = 1   # 1 is reject
        report.save()
        return UTF8JsonResponse(data={'status': 1, 'errno': 4006, 'msg': "成功拒绝申诉学者记录"})

    # when it is rejecting article
    try:
        article = searchPaper(report.reportArticle_id)['results'][0][0]
    except:
        article = None

    if article is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4001, 'msg': "学术成果不存在"})

    # Notification    
    newNotice = Notification(type=9, belongTo=user, paperId=article['id'], paperName=article['title'], scholarId=scholar['id'], scholarName=scholar['name'])
    newNotice.save()

    report.result = 1   # 1 is reject
    report.save()
    return UTF8JsonResponse(data={'status': 1, 'errno': 4006, 'msg': "成功拒绝申诉学术成果记录"})

@csrf_exempt
def acceptReport(request, reportId):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
    user = get_auth_user(uid)
    if user is None or not user.is_staff:
        return UTF8JsonResponse(data={'errno': 4010, 'msg': '不是管理员，不能操作'})

    report = Report.objects.filter(id=reportId).first()

    if report is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4004, 'msg': "申诉记录不存在"})
    if report.result != 0:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4005, 'msg': "无法修改申诉记录，因为其已经是在接受或者拒绝状态"})

    # get the scholar info from ES
    try:
        scholar = searchAuthor(report.reportScholar_id)['results'][0][0]
    except:
        scholar = None

    if scholar is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4002, 'msg': "学者不存在"})

    # when it is accepting scholar
    if report.category == 1:

        userPerspective = UserAuthenticateScholar.objects.filter(user_id=user.id).first()

        if userPerspective is not None:
            return UTF8JsonResponse({'errno': 4014, 'msg': "该用户已经认领学者门户，不能再认领"})

        userAuthScholar = UserAuthenticateScholar.objects.filter(scholar_id=scholar["id"]).first()

        if userAuthScholar is None:
            return UTF8JsonResponse({'errno': 4013, 'msg': "该学者门户还没认领，可以认领，不用申诉"})

        if userAuthScholar is not None and userAuthScholar.user_id == user.id and userAuthScholar.scholar == scholar['id']:
            return UTF8JsonResponse({'errno': 4014, 'msg': "该用户已经认领该学者门户"})

        # change ownership
        secondPartyUser = get_auth_user(userAuthScholar.user_id)
        secondPartyUser.scholarAuth = None

        user.scholarAuth = userAuthScholar.scholar_id

        userAuthScholar.user_id = user.id
        secondPartyUser.save()
        user.save()
        userAuthScholar.save()

        newNotice = Notification(type=6, belongTo=user, scholarId=scholar['id'], scholarName=scholar['name'])
        newNotice.save()

        report.result = 2   # 2 is accept
        report.save()
        return UTF8JsonResponse(data={'status': 1, 'errno': 4006, 'msg': "成功接受申诉学者记录"})

    # when it is accepting article
    try:
        article = searchPaper(report.reportArticle_id)['results'][0][0]
    except:
        article = None

    if article is None:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4001, 'msg': "学术成果不存在"})

    # find whether the reported Scholar is in the article
    scholarsInArticle = [author["id"] for author in article['authors']]

    if scholar['id'] not in scholarsInArticle:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4015, 'msg': "该学者并不是该学术成果的作者"})


    # todo Update the report in ES


    # Notification    
    newNotice = Notification(type=9, belongTo=user, paperId=article['id'], paperName=article['title'], scholarId=scholar['id'], scholarName=scholar['name'])
    newNotice.save()
    
    report.result = 2   # 2 is accept
    report.save()
    return UTF8JsonResponse(data={'status': 1, 'errno': 4006, 'msg': "成功接受申诉学术成果记录"})


@csrf_exempt
def changeReportStatus(request, result, reportId):
    if request.method != 'POST':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是POST'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
    user = get_auth_user(uid)
    if user is None or not user.is_staff:
        return UTF8JsonResponse(data={'errno': 4010, 'msg': '不是管理员，不能操作'})

    report = Report.objects.filter(id=reportId).first()

    if not report:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4004, 'msg': "申诉记录不存在"})
    if report.result != 0:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4005, 'msg': "无法修改申诉记录，因为其已经是在接受或者拒绝状态"})

    # When reject
    if result == 1:
        # when it is scholar report
        if report.category == 1:
            # scholar = Scholar.objects.filter(id=report.reportScholar_id).first()
            # get the scholar info from ES
            try:
                scholar = searchAuthor(report.reportScholar_id)['results'][0][0]
            except:
                scholar = None

            newNotice = Notification(type=6, belongTo=user, scholarId=scholar.id, scholarName=scholar.name)
            newNotice.save()
            return UTF8JsonResponse(data={'status': 1, 'category': report.category, 'errno': 4006, 'msg': "成果拒绝申诉记录"})

        #when it is article
        



    # when result == 2, it is accepted
    # when it is scholar report
    if report.category == 1:
        # todo remove ownership of scholar from the current specificed owner and change ownership of scholar to the report owner.
        # if user already have scholar
        if user.scholarAuth is not None:
            return UTF8JsonResponse({'errno': 4011, 'msg': "用户已有学者门户，不能再申诉"})

        # scholar = Scholar.objects.filter(id=report.reportScholar_id).first()
        # get the scholar info from ES
        try:
            scholar = searchAuthor(report.reportScholar_id)['results'][0][0]
        except:
            scholar = None
        
        # if scholar not exits (might be it was deleted or it is null now)
        if scholar is None:
            return UTF8JsonResponse({'errno': 4012, 'msg': "学者已经不存在"})

        # if no one authenticate scholar yet
        if scholar.belongTo is None:
            return UTF8JsonResponse({'errno': 4013, 'msg': "该学者门户还没认领，可以认领，不用申诉"})

        # get the user initially own that scholar, then reassign it's belongTo property to None before changing schoar belongTo's property
        # secondPartyUser = CustomUser.objects.filter(scholar.belongTo_id).first()
        secondPartyUser = scholar.belongTo
        if secondPartyUser:
            secondPartyUser.scholarAuth = None
            secondPartyUser.belongTo = None
            secondPartyUser.save()
        
        scholar.belongTo = user
        user.scholarAuth = scholar.id
        scholar.save()
        user.save()

        newNotice = Notification(type=5, belongTo=user, scholarId=scholar.id, scholarName=scholar.name)
        newNotice.save()


    elif report.category == 2:
        # todo remove ownersip of article from the current specified owner and change ownership of article to the report owner
        
        pass

    report.result = result
    report.save()
    return UTF8JsonResponse(data={'status': 1, 'category': report.category, 'errno': 4006, 'msg': "成果接受申诉记录"})


# Get all reports
@csrf_exempt
def getAllScholarReports(request):
    if request.method != 'GET':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是GET'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    return getAllReports(request, 1)

@csrf_exempt
def getAllArticleReports(request):
    if request.method != 'GET':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是GET'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    return getAllReports(request, 2)

@csrf_exempt
def getAllReports(request, category):
    queryParams = request.GET.dict()
    result = None
    if queryParams.get('status') is not None and queryParams.get('status') >= '0' and queryParams.get('status') <= '2':
        result = queryParams.get('status');

    if result:
        reports = Report.objects.filter(category=category, result=result)
    else:
        reports = Report.objects.filter(category=category)

    allReports = []
    for report in reports:
        tmp = model_to_dict(report)
        tmp['id'] = report.id
        allReports.append(tmp)

    return UTF8JsonResponse(data={'status': 1, 'reports': allReports, 'errno': 4007, 'msg': "成果读取申诉记录"})

@csrf_exempt
def getBothReports(request):
    if request.method != 'GET':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是GET'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})

    queryParams = request.GET.dict()
    result = None
    if queryParams.get('status') is not None and queryParams.get('status') >= '0' and queryParams.get('status') <= '2':
        result = queryParams.get('status');

    if result:
        reports = Report.objects.filter(result=result)
    else:
        reports = Report.objects.filter()

    allReports = []
    for report in reports:
        tmp = model_to_dict(report)
        tmp['id'] = report.id
        allReports.append(tmp)

    return UTF8JsonResponse(data={'status': 1, 'reports': allReports, 'errno': 4007, 'msg': "成果读取申诉记录"})


# Get single report
@csrf_exempt
def getReportById(request, reportId):
    if request.method != 'GET':
        return UTF8JsonResponse(data={'errno': 800002, 'msg': '请求格式有误，不是GET'})
    uid = request.session.get('uid')
    if uid is None:
        return UTF8JsonResponse(data={'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
    report = Report.objects.filter(id=reportId).first()
    if not report:
        return UTF8JsonResponse(data={'status': 0, 'errno': 4004, 'msg': "申诉记录不存在"})
    
    tmp = model_to_dict(report)
    tmp['id'] = report.id
    return UTF8JsonResponse(data={'status': 1, 'reports': tmp, 'errno': 4007, 'msg': "成果读取申诉记录"})

