# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 0:29
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : adminx.py.py
# @Software: PyCharm
from .models import Course,Lesson,Video,CourseResource
import xadmin

class LessonInlines(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['CourseName','degree','CourseType','Students','FavouriteNumber','ClikeNumber','AddTime']
    search_fields = ['CourseName','degree','CourseType','Students','FavouriteNumber','ClikeNumber']
    list_filter = ['CourseName','degree','CourseType','Students','FavouriteNumber','ClikeNumber','AddTime']
    inlines = [LessonInlines]

#利用 admin.site.register 进行注册
xadmin.site.register(Course,CourseAdmin)

class LessonAdmin(object):
    list_display = ['Course','LessonName','AddTime']
    search_fields = ['Course','LessonName']
    #要在过滤条件中显示外键的子内容时，用双下划线
    list_filter = ['Course__CourseName','LessonName','AddTime']
    list_editable = ['LessonName']
    refresh_times = [3, 5]  # 列表内的刷新时间的选择

#利用 admin.site.register 进行注册
xadmin.site.register(Lesson,LessonAdmin)

class VideoAdmin(object):
    list_display = ['LessonName','VideoName','VideoUrl','AddTime']
    search_fields = ['LessonName','VideoUrl','VideoName']
    #要在过滤条件中显示外键的子内容时，用双下划线
    list_filter = ['LessonName','VideoName','VideoUrl','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(Video,VideoAdmin)

class CourseResourceAdmin(object):
    list_display = ['Course','Name','DownLoad','AddTime']
    search_fields = ['Course','Name','DownLoad']
    #要在过滤条件中显示外键的子内容时，用双下划线
    list_filter = ['Course','Name','DownLoad','AddTime']

#利用 admin.site.register 进行注册
xadmin.site.register(CourseResource,CourseResourceAdmin)