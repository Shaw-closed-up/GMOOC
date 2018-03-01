# -*- coding: utf-8 -*-
# @Time    : 2018/1/27 16:22
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : url.py
# @Software: PyCharm

from django.conf.urls import url,include
from .views import CoursesListView,CourseDetailView,CourseVideoView,CourseCommentView,CourseAddCommentView,VideoPlayView

urlpatterns = [
    url(r'^courses_list/$', CoursesListView.as_view(), name='courses_list'),
    url(r'^courses_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^courses_video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^courses_comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='courses_comment'),
    url(r'^courses_add_comment/$', CourseAddCommentView.as_view(), name='courses_add_comment'),
    url(r'^video_play/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]