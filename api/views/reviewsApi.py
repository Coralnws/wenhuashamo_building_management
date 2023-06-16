from datetime import timedelta
from datetime import datetime
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils import timezone
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from ..utils import *
from api.search import *
from django.forms.models import model_to_dict



#createReview
#getReview

# @csrf_exempt
# def createArticleReview(request):
#     if request.method == 'POST':
#         userId = request.POST.get('userId')
#         articleId = request.POST.get('paperId')
#         content = request.POST.get('content')
#         user = CustomUser.objects.filter(id=userId).first()

#         newReview = Review(article=articleId,content=content,createdBy=user)
#         newReview.save()

#         data = searchPaperAuthor(articleId)
            
#         name = data[0]
#         print("name:"+name)
#         authorList = data[1]

#         for tmp in authorList:
#             if 'id' in tmp: 
#                 scholarUser = CustomUser.objects.filter(scholarAuth=tmp['id']).first()
#                 newNotice = Notification(type=10,belongTo=scholarUser,userId=userId,userName=user.username,paperId=articleId,paperName=name)
#                 newNotice.save()

#         return UTF8JsonResponse({'errno':1001, 'msg': '成功发布评论'})

@csrf_exempt
def createReview(request):
    if request.method == 'POST':
        userId=request.session.get('uid')
        if userId is None:
            return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        # userId = request.POST.get('userId')
        reviewId = request.POST.get('reviewId')
        paperId = request.POST.get('paperId')
        content = request.POST.get('content')
        atUserId = request.POST.get('atUserId')



        user = CustomUser.objects.filter(id=userId).first()
        
        if user.banComment:
            if user.banDuration > timezone.now():
                data={}
                data['banDuration'] = user.banDuration
                return UTF8JsonResponse({'errno':3001, 'msg': '用户已被禁言','data':data})
            else:
                user.banComment=False
                user.banDuration=None
        if reviewId is not None:  #reply
            review = Review.objects.filter(id=reviewId).first()
            if atUserId is not None:
                atUser = CustomUser.objects.filter(id=atUserId).first()
                newReview = Review(review=review,content=content,createdBy=user,atUser=atUser)
                newReview.save()
            else:
                newReview = Review(review=review,content=content,createdBy=user)
                newReview.save()

            # notifyUser = review.createdBy

            # data = searchPaperAuthor(paperId)
            # name = data[0]

            
                
            # newNotice = Notification(type=11,belongTo=notifyUser,userId=userId,userName=user.username,paperId=paperId,paperName=name,reviewId=reviewId)
            # newNotice.save()

            data=model_to_dict(newReview)
            data['id'] = newReview.id 
            # data2=model_to_dict(newNotice)
            data2=[]
            return UTF8JsonResponse({'errno':1001, 'msg': '成功回复评论','review':data,'notification':data2})
        else:
            newReview = Review(article=paperId,content=content,createdBy=user)
            newReview.save()

            # data = searchPaperAuthor(paperId)
                
            # name = data[0]
            # print("name:"+name)
            # authorList = data[1]

            # for tmp in authorList:
            #     if 'id' in tmp: 
            #         scholarUser = CustomUser.objects.filter(scholarAuth=tmp['id']).first()
            #         newNotice = Notification(type=10,belongTo=scholarUser,userId=userId,userName=user.username,paperId=paperId,paperName=name)
            #         newNotice.save()

            data=model_to_dict(newReview)
            data['id'] = newReview.id 
            # data2=model_to_dict(newNotice)
            data2=[]
            return UTF8JsonResponse({'errno':1001, 'msg': '成功发布评论','review':data,'notification':data2})


@csrf_exempt
def getReview(request):
    if request.method == 'GET':
        paperId = request.GET.get('paperId','')
        if paperId is None:
            return UTF8JsonResponse({'errno':3001, 'msg': '无paperId'})
        reviewList = Review.objects.filter(article=paperId) 


        reviewListData=[]
        for review in reviewList:
            print(review)
            creator=review.createdBy
            reviewData={}
            reviewData['commentId']=review.id
            reviewData['userId']= creator.id
            reviewData['username'] = creator.username
            reviewData['content']=review.content
            reviewData['avatar']="image_url"
            reviewData['time']=review.createdAt.strftime("%d-%m-%Y %H:%M:%S")

            replyList=Review.objects.filter(review=review)
            replyListData=[]
            for reply in replyList:
                replyData={}
                creator=reply.createdBy
                atUser=reply.atUser
                replyData['commentId']=reply.id
                replyData['userId']= creator.id
                replyData['username'] = creator.username
                replyData['content']=reply.content
                if atUser:
                    replyData['atUserName']=atUser.username
                else:
                    replyData['atUserName']=None
                replyData['avatar']="image_url"
                replyData['time']=reply.createdAt.strftime("%d-%m-%Y %H:%M:%S")
                replyListData.append(replyData)
            
            reviewData['reply']=replyListData

            reviewListData.append(reviewData)
    
        return UTF8JsonResponse({'errno':1001, 'msg': '返回评论成功', 'data': reviewListData})


@csrf_exempt
def reportReview(request):
    if request.method == 'POST':
        userId=request.session.get('uid')
        if userId is None:
            return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        #userId = request.POST.get('userId')

        reviewId = request.POST.get('reviewId')

        type = request.POST.get('type')
        user = CustomUser.objects.filter(id=userId).first()

        review = Review.objects.filter(id=reviewId).first()

        newReport = ReviewReport(reportReview=review,category=type,createdBy=user)

        newReport.save()

        data=model_to_dict(newReport)
        
        return UTF8JsonResponse({'errno':1001, 'msg': '成功举报评论','data':data})

@csrf_exempt
def manageReviewReport(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        userStaff = CustomUser.objects.filter(id=userId).first()
        if userStaff.is_staff == False:
            return UTF8JsonResponse({'errno':3001, 'msg': '非管理员'})
        reportId = request.POST.get('reportId')
        report=ReviewReport.objects.filter(id=reportId).first()
        review = report.reportReview
        user = CustomUser.objects.filter(id=review.createdBy.id).first()
        
        result = request.POST.get('result') #0=decline ,1=accept
        articleId = review.article
        data = searchPaperAuthor(articleId)
            
        name = data[0]
        if result == '1':
            user.banComment = True
            user.banDuration = timezone.now() + timezone.timedelta(days=3)
            user.save()
            report.result=True
            noticeToCreator = Notification(type=12,belongTo=user,paperId=articleId,paperName=name)
            noticeToCreator.save()
            noticeToUser = Notification(type=13,belongTo=report.createdBy,paperId=articleId,paperName=name,userId=user.id,userName=user.username)
            noticeToUser.save()

            review.delete()
            data=model_to_dict(noticeToUser)
            data1=model_to_dict(noticeToCreator)
            return UTF8JsonResponse({'errno':1001, 'msg': '举报通过，已将用户禁言三天','noticeToReviewCreator':data1,'noticeToReportCreator':data})
        elif result == '0':
            report.result=False
            noticeToUser = Notification(type=14,belongTo=report.createdBy,paperId=articleId,paperName=name,userId=user.id,userName=user.username)
            noticeToUser.save()
            data=model_to_dict(noticeToUser)
            return UTF8JsonResponse({'errno':2001, 'msg': '举报驳回','notification':data})

@csrf_exempt
def deleteReview(request):
    if request.method == 'POST':
        userId=request.session.get('uid')
        if userId is None:
            return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        reviewId=request.POST.get('reviewId')
        review = Review.objects.filter(id=reviewId).first()
        user= CustomUser.objects.filter(id=userId).first()
        if review.createdBy == user:
            review.delete()
            return UTF8JsonResponse({'errno':1001, 'msg': '成功删除评论'})
        else:
            return UTF8JsonResponse({'errno':2001, 'msg': '非本人操作'})