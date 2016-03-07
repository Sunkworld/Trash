FROM_EMAIL_HOST = 'smtp.gmail.com'
FROM_EMAIL_PORT = 587
EMAIL_USER = 'es.aptx4869'
EMAIL_PASSWD = ''
TO_EMAIL = '365062829@qq.com'
DESTINATED_WEIBO = ['', '']    #微博id列表

RELAX_TIME = 1000     #刷新时间，单位为s
CHK_WEIBO = 1        #定时检查微博
CHK_WEIBO_DELETED = 1      #有微博被删时通知
CHK_PROFILE = 1        #检查简介
CHK_FOLLOW = 1         #检查TA关注的用户
CHK_FANS = 1          #检查TA的粉丝
AUTO_LIKE = 0        #自动点赞
