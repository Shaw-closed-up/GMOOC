# -*- coding: utf-8 -*-
# @Time    : 2018/2/18 18:22
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : url.py
# @Software: PyCharm
from django.conf.urls import url,include
from .views import UserInfoView,UserImgUploadView,UserPasswordUpdateView,EmailCodeView,UpdateEmailView,MyCourseView,MyFavView,MyMessageView

urlpatterns = [
    url(r'^user_info/$', UserInfoView.as_view(), name='user_info'),

    #用户头像上传/更新
    url(r'^user_img_upload/$', UserImgUploadView.as_view(), name='user_img_upload'),

    #用户密码修改
    url(r'^password_update/$', UserPasswordUpdateView.as_view(), name='password_update'),

    #接收邮箱验证码
    url(r'^send_email_code/$', EmailCodeView.as_view(), name='send_email_code'),

    #修改个人中心邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    #我的课程
    url(r'^my_courses/$', MyCourseView.as_view(), name='my_courses'),

    # 我的收藏
    url(r'^my_fav/$', MyFavView.as_view(), name='my_fav'),

    # 我的信息
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),
]