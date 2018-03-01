#_*_ conding:utf-8 _*_
from django.db import models
#auth_user的类
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from organization.models import CourseOrganization,Teacher
#from DjangoUeditor.models import UEditorField

# Create your models here.

class Course(models.Model):
    Organization = models.ForeignKey(CourseOrganization,verbose_name=u'所属机构',null=True,blank=True)
    Describe = models.CharField(verbose_name=u'课程简介',max_length=500)
    CourseName = models.CharField(max_length=100,verbose_name=u'课程名称')
    Detail = models.TextField(verbose_name=u'课程详情')
    #Detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, toolbars="full", imagePath="course/detail/img", filePath="course/detail/file",default='')
    Display = models.BooleanField(default=False,verbose_name=u'展示与否')
    degree = models.CharField(max_length=10,verbose_name=u'课程难度',choices=(('cj',u'初级'),('zj',u'中级'),('gj',u'高级')))
    LearnTime = models.IntegerField(verbose_name=u'学习时长',default=0)
    CourseType = models.CharField(max_length=30,verbose_name=u'课程类型')
    #LearnUser = models.ImageField(upload_to='static/Pic/courses/%Y/%m',max_length=500,verbose_name=u'学习用户')
    CoursePicture = models.ImageField(upload_to='courses/%Y/%m',max_length=500,verbose_name=u'课程封面')
    Students = models.IntegerField(default=0,verbose_name=u'学习人数')
    FavouriteNumber = models.IntegerField(default=0,verbose_name=u'喜欢人数')
    ClikeNumber = models.IntegerField(default=0,verbose_name=u'点击人数')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间',)
    Tag = models.CharField(default='',max_length=10,verbose_name=u'标签',null=True,blank=True)
    Teacher = models.ForeignKey(Teacher,verbose_name=u'课程老师',null=True,blank=True)
    YouNeedKonw = models.CharField(default='',max_length=300,verbose_name=u'课程须知',null=True,blank=True)
    TeacherTellYou = models.CharField(default='',max_length=300,verbose_name=u'老师告诉你的',null=True,blank=True)

    def __str__(self):
        return '{0}'.format(self.CourseName)

    def get_lesson_nums(self):
        """
        course作为lesson的外键，利用self.lesson_set获取lesson参数
        """
        lesson_num = self.lesson_set.all().count()
        return lesson_num

    def get_study_user(self):
        study_user = self.usercourse_set.all()[:5]
        return study_user

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    LessonName = models.CharField(max_length=100,verbose_name=u'章节名称',default='未命名',null=True,blank=True)
    Course = models.ForeignKey(Course,verbose_name=u'课程名称')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.LessonName)

    #获取各个章节下的课程video
    def get_video(self):
        video = self.video_set.all()
        return video

class Video(models.Model):
    LessonName = models.ForeignKey(Lesson,verbose_name=u'章节名称',default='未命名',)
    VideoName = models.CharField(max_length=100, verbose_name=u'视频名称')
    AddTime = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    VideoUrl = models.CharField(default='',verbose_name='播放路径',max_length=200,null=True,blank=True) #播放地址
    LearnTime = models.IntegerField(verbose_name=u'学习时长',default=0)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.VideoName)



class CourseResource(models.Model):
    Course = models.ForeignKey(Course, verbose_name=u'课程')
    Name = models.CharField(max_length=100, verbose_name=u'名称')
    DownLoad = models.FileField(upload_to='course/resource/%Y/%m/%d',max_length=100, verbose_name=u'下载')
    AddTime = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
