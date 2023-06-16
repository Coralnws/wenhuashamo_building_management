from django.urls import path
from api.views import scholarAuthentication, articleAuthentication, reportController, userManage,scholarCommunicate,notificationApi,reviewsApi,questionApi, es,userArticle,scholarPage, userCollection,userHistory

urlpatterns = [
    # User Authentication
    path('register', userManage.register),
    path('login', userManage.login),
    path('logout', userManage.logout),
    path('updateInfo', userManage.updateInfo),
    path('getUserMsg', userManage.getUserMsg),
    path('addThumbnail', userManage.addThumbnail),
    path('changePassword', userManage.changePassword),
    path('forgotPassword', userManage.forgotPassword),
    path('getQuestion', userManage.getQuestion),



    # Scholar Authentication
    path('scholar/request', scholarAuthentication.requestScholarAuthenticate),
    path('scholar/validate', scholarAuthentication.validateScholarAuthenticate),

    # Article Authentication
    path('article/request', articleAuthentication.requestArticleAuthenticate),
    path('article/validate', articleAuthentication.validateArticleAuthenticate),

    # report scholar and scholar article
    path('report/scholar', reportController.reportScholar),
    path('report/article', reportController.reportArticle),
    path('report/accept/<uuid:reportId>', reportController.acceptReport),
    path('report/reject/<uuid:reportId>', reportController.rejectReport),
    path('report/get/<uuid:reportId>', reportController.getReportById),
    path('report/scholar/all', reportController.getAllScholarReports),
    path('report/article/all', reportController.getAllArticleReports),
    path('report/all', reportController.getBothReports),

    #follow scholar
    path('follow/',scholarCommunicate.followScholar),
    path('getFollowList/',scholarCommunicate.getFollowList),

        #private message
    path('requestPM',scholarCommunicate.requestPrivateMessage),
    path('getChatBoxList',scholarCommunicate.getRequest),
    path('replyRequest',scholarCommunicate.replyRequest),
    path('getChatBoxMessage',scholarCommunicate.getChatBoxMessage),
    path('sendMessage',scholarCommunicate.sendMessage),

    #notification
    path('getNotification',notificationApi.getNotification),
    path('checkNotification',notificationApi.checkNotification),
    path('delNotification',notificationApi.deleteNotification),
    
    #review
    #path('reviewArticle',reviewsApi.createArticleReview),
    path('createReview',reviewsApi.createReview),
    path('getReviewList',reviewsApi.getReview),
    path('reportReview',reviewsApi.reportReview),
    path('manageReviewReport',reviewsApi.manageReviewReport),
    path('deleteReview',reviewsApi.deleteReview),

    #question
    path('createQuestion',questionApi.createQuestionReply),
    #path('getQuestion',questionApi.getQuestionReply),

    #es query
    path('esQPaper', es.QPaper),
    path('esQAuthor',es.QAuthor),
    path('esAdvancedQ',es.AdvancedQ),

    #userArticle
    path('bookmark',userArticle.bookmarkArticle),
    path('createHistory',userArticle.createHistory),
    path('getBookmarkList',userArticle.getBookmarkList),
    path('getHistoryList',userArticle.getHistoryList),

    #page
    path('getScholarPage',es.getAuthorById),
    path('getPaperPage',es.getPaperById),

    #frontPage
    path('getAuthorRank',es.AuthorRank),

    #userHistory
    path('addHistory',userHistory.addHistory),
    path('viewHistory', userHistory.viewHistory),

    #userCollection
    path('addCollection', userCollection.addCollection),
    path('viewCollection', userCollection.viewCollection),
    path('cancelCollection', userCollection.cancelCollection),
]