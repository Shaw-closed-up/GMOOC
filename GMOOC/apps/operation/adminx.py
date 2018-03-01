# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 22:06
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : adminx.py
# @Software: PyCharm

from .models import UserAsk,CourseComment,UserFavorite,UserMessage,UserCourse
import xadmin

class UserAskAdmin(object):
    list_display = ['UserName','MobileNumber','CourseName','AddTime']
    search_fields = ['UserName','MobileNumber','CourseName']
    list_filter = ['UserName','MobileNumber','CourseName','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(UserAsk,UserAskAdmin)

class CourseCommentAdmin(object):
    list_display = ['User','Course','Comment','AddTime']
    search_fields = ['User','Course','Comment']
    list_filter = ['User','Course','Comment','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(CourseComment,CourseCommentAdmin)

class UserFavoriteAdmin(object):
    list_display = ['User','FavoriteID','FavoriteType','AddTime']
    search_fields = ['User','FavoriteID','FavoriteType']
    list_filter = ['User','FavoriteID','FavoriteType','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(UserFavorite,UserFavoriteAdmin)


class UserMessageAdmin(object):
    list_display = ['User','message','HasRead','AddTime']
    search_fields = ['User','message','HasRead']
    list_filter = ['User','message','HasRead','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(UserMessage,UserMessageAdmin)

class UserCourseAdmin(object):
    list_display = ['User','Course','AddTime']
    search_fields = ['User','Course']
    list_filter = ['User','Course','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(UserCourse,UserCourseAdmin)