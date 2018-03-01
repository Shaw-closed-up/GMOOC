#_*_ conding:utf-8 _*_
from django.db import models
#auth_user的类
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from users.models import UserProfile
from courses.models import Course
# Create your models here.

class UserAsk(models.Model):
    UserName = models.CharField(max_length=20,verbose_name=u'用户名称')
    MobileNumber = models.CharField(max_length=11,verbose_name=u'用户电话')
    CourseName = models.CharField(max_length=50,verbose_name=u'课程名称')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural =verbose_name


class CourseComment(models.Model):
    User = models.ForeignKey(UserProfile,verbose_name=u'用户')
    Course = models.ForeignKey(Course,verbose_name=u'课程')
    Comment = models.CharField(max_length=200,verbose_name=u'用户评论')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural =verbose_name


class UserFavorite(models.Model):
    User = models.ForeignKey(UserProfile,verbose_name=u'用户')
    #为了少增加数据条目，所以用  FavoriteID 和 FavoriteType 来控制收藏类型和收藏的ID
    FavoriteType = models.IntegerField(choices=((1,'课程'),(2,'机构'),(3,'教师')))
    FavoriteID = models.IntegerField(default=0,verbose_name=u'数据ID')    #根据FavoriteType来定的id，若收藏的是课程则保存课程的id，若收藏的是机构则保存机构的id
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural =verbose_name


class UserMessage(models.Model):
    # user使用IntegerField,"0"指代给所有人发送信息，可以用数字分别设定给哪一群人发送信息，为用户ID时，指代给某位用户发送信息
    User = models.IntegerField(default=0,verbose_name=u'用户')
    message = models.CharField(max_length=500,verbose_name=u'信息')
    HasRead = models.BooleanField(default=False,verbose_name=u'是否已读')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural =verbose_name


class UserCourse(models.Model):
    User = models.ForeignKey(UserProfile,verbose_name=u'用户')
    Course = models.ForeignKey(Course,verbose_name=u'课程')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural =verbose_name
