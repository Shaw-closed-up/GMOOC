# -*- coding: utf-8 -*-
# @Time    : 2018/2/18 1:27
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : url_son.py
# @Software: PyCharm
from django.conf.urls import url,include
from .views import OrganiztionListView,UserAskView,OrganiztionDetailView,OrganiztionCourseView,OrganiztionDescribeView,OrganiztionTeacherlView,AddFavView,TeacherListView,TeacherDetailView,TeacherDetailTestView

urlpatterns = [
    #教师详情页
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailTestView.as_view(), name='teacher_detail'),

]