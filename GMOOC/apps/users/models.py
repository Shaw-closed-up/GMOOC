#_*_ conding:utf-8 _*_
from django.db import models
#auth_user的类
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

#  继承AbstractUser等于继承auth_user数据表的类
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u"外号",default='')
    birthday = models.DateField(verbose_name=u'生日日期',null=True,blank=True)
    gender = models.CharField(max_length=6,choices=(('male',u'男'),('female','女')),default=u'女',verbose_name=u'性别')
    adress = models.CharField(max_length=100,default=u'',verbose_name=u'地址')
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name=u'电话')
    img = models.ImageField(upload_to='user_img/%Y/%m',default='image/def ault.png',verbose_name=u'头像')
    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name
        db_table = 'users'


class EmailVerifyCode(models.Model):
    code = models.CharField(max_length=20,verbose_name='验证码')
    email = models.EmailField(max_length=30,verbose_name='邮箱')
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')  #注意是now而不是now()
    send_type = models.CharField(choices=(('reguster',u'注册'),('forget',u'忘记密码'),('update',u'更新邮箱')),max_length=20,verbose_name=u'发送类型')
    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.email)

class Banner(models.Model):
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    img = models.ImageField(upload_to='static/Pic/Banner/%Y/%m/%d',default='Banner/default.png',verbose_name=u'轮播图')
    index = models.IntegerField(default=100,verbose_name=u'序号')
    title = models.CharField(max_length=100,verbose_name=u'标题')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'图片录入时间')
    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name