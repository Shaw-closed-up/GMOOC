# -*- coding: utf-8 -*-
# @Time    : 2018/1/17 0:35
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : url.py
# @Software: PyCharm
from django.conf.urls import url,include
from .views import OrganiztionListView,UserAskView,OrganiztionDetailView,OrganiztionCourseView,OrganiztionDescribeView,OrganiztionTeacherlView,AddFavView,TeacherListView,TeacherDetailView

urlpatterns = [
    url(r'^organization_list/$', OrganiztionListView.as_view(), name='organiztion_list'),
    url(r'^user_ask/$', UserAskView.as_view(), name='user_ask'),    #用户咨询post地址
    url(r'^organization_home/(?P<org_id>\d+)/$', OrganiztionDetailView.as_view(), name='organization_home'),
    url(r'^organization_course/(?P<org_id>\d+)/$', OrganiztionCourseView.as_view(), name='organization_course'),
    url(r'^organization_teacher/(?P<org_id>\d+)/$', OrganiztionTeacherlView.as_view(), name='organization_teacher'),
    url(r'^organization_describe/(?P<org_id>\d+)/$', OrganiztionDescribeView.as_view(), name='organization_describe'),
    url(r'^user_fav/$', AddFavView.as_view(), name='user_fav'),    #用户收藏post地址

    # 教师列表页
    url(r'^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),

    #教师详情页
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
    #url(r'^teacher_list_test/', include('organization.url_son', namespace='url_son')),

]