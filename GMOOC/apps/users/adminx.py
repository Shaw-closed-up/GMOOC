# -*- coding: utf-8 -*-
# @Time    : 2017/11/13 23:19
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : adminx.py.py
# @Software: PyCharm
from django.contrib import admin
from .models import UserProfile,EmailVerifyCode,Banner,UserProfile
import xadmin
from xadmin import views
# class UserProfileAdmin(object):
#     list_display = ['nick_name','birthday','gender','adress','mobile','img']
#     search_fields = ['nick_name','birthday','gender','adress','mobile','img']
#     list_filter = ['nick_name','birthday','gender','adress','mobile','img']
# #利用 admin.site.register 进行注册
# xadmin.site.register(UserProfile,UserProfileAdmin)


# class UserProfileAdmin(object):
#     list_display = ['nick_name','birthday','gender','adress']
#     search_fields = ['nick_name','birthday','gender','adress']
#     list_filter = ['nick_name','birthday','gender','adress']
# #利用 admin.site.register 进行注册
# xadmin.site.register(UserProfile,UserAdmin)



class EmailVerifyCodeAdmin(object):
    list_display = ['code','email','send_time','send_type']
    search_fields = ['code','email','send_time']
    list_filter = ['code','email','send_time']
    model_icon = 'fa fa-user-circle-o'   #图例修改
    ordering = ['-code']    #排序
    readonly_fields = ['code','email']  #只读
    #exclude = ['send_time'] #隐藏状态

#利用 admin.site.register 进行注册
xadmin.site.register(EmailVerifyCode,EmailVerifyCodeAdmin)


class BannerAdmin(object):
    list_display = ['url','img','index','title','add_time']
    search_fields = ['url','img','index','title']
    list_filter = ['url','img','index','title']
    pass
#利用 admin.site.register 进行注册
xadmin.site.register(Banner,BannerAdmin)

class BaseSetting(object):
    #主题功能，多种主题
    enable_themes = True
    use_bootswatch = True

#注册BaseSetting，需要与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)

class GlobalSettings(object):
    #后台系统头部标签
    site_title = "张馨"
    #后台系统底部标签
    site_footer = "叶嘉"
    #菜单抽屉效果
    menu_style = "accordion"
xadmin.site.register(views.CommAdminView,GlobalSettings)

# #注销注册
# from django.contrib.auth.models import User
# xadmin.site.unregister(User)