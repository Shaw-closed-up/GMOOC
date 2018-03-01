"""GMOOC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
#处理静态文件
from django.views.generic import TemplateView
import xadmin
import crispy_forms
#from users.views import user_login
from users.views import *
from organization.views import OrganiztionListView
from django.views.static import serve
from GMOOC.settings import MEDIA_ROOT,STATICFILES_DIRS
from users.views import IndexView


#错误页面配置
handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^$',IndexView.as_view(),name='index'),
    #传入user_login句柄，指向user_login
    #url(r'^login/$', user_login, name='user_login'),
    url(r'^login/$', LoginView.as_view(), name='user_login'),
    #######################新增注销功能######################
    url(r'^loginout/$', logout_view, name='user_loginout'),
    #########################################################
    url(r'^register/$', RegisterView.as_view(), name='Register'),
    url(r'^captcha/', include('captcha.urls')), #定义图片位置
    #写入注册激活地址，通过url获取激活验证码，注意书写规范
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='active_user'),
    url(r'^forgetpwd/$', ForgetpwdView.as_view(), name='forgetpwd'),
    url(r'^password_reset/(?P<active_code>.*)/$', PasswordReset.as_view(), name='password_reset'),
    #####################organization模板复用#######################
    #url(r'organiztion_list/$',OrganiztionListView.as_view(),name='organiztion_list'),
    #url(r'organiztion_list/$', TemplateView.as_view(template_name='org_list.html'), name='organiztion_list'),  #测试

    ######################机构列表##########################################
    url(r'^organization/', include('organization.url',namespace='organization')),  # organiztion 的url分发,namespace用于重名的处理
    ######################课程列表##########################################
    url(r'^courses/', include('courses.url', namespace='courses')), # organiztion 的url分发,namespace用于重名的处理

    ############################################配置动态上传图片资源的访问处理函数#######################################
    url(r'^media/(?P<path>.*)/$', serve, {"document_root":MEDIA_ROOT},name='img_path'),
    #url(r'^static/(?P<path>.*)/$', serve, {"document_root": STATICFILES_DIRS}, name='static_path'),    #直接影响到了静态文件的寻址路径

    ############################################处理机构详情#######################################
    url(r'^forgetpwd/$', ForgetpwdView.as_view(), name='forgetpwd'),

    url(r'^user_center/', include('users.url', namespace='user_info')),# organiztion 的url分发,namespace用于重名的处理

    #富文本相关url
    #url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

'''
user_login和user_login()区别：
user_login代表指向这个函数
user_login()代表调用这个函数
LoginView.as_view():把LoginView类转换为一个as_view,返回一个函数句柄,此处要调用用方法，所以要()。
(?P):提取一个变量当做参数
(?P<active_code>.*):正则表达式.*匹配到的内容填充到<active_code>中
'''