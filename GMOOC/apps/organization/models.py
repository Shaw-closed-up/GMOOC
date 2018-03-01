#_*_ conding:utf-8 _*_
from django.db import models
#auth_user的类
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class CityDict(models.Model):
    CityName = models.CharField(max_length=20,verbose_name=u'城市名称')
    CityDescribe = models.TextField(verbose_name=u'城市描述')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural =verbose_name

    def __str__(self):
        return '{0}'.format(self.CityName)

class CourseOrganization(models.Model):
    Organization = models.CharField(max_length=50,verbose_name=u'组织名称')
    OrganizationDescribe = models.TextField(verbose_name=u'组织描述')
    ClickNumber = models.IntegerField(verbose_name=u'点击数',default=0)
    FavoriteNumber = models.IntegerField(verbose_name=u'收藏数',default=0)
    OrganizationImage = models.ImageField(upload_to='org/%Y/%m',verbose_name=u'组织封面')
    Address = models.CharField(max_length=200,verbose_name=u'组织地址')
    City = models.ForeignKey(CityDict,verbose_name=u'所属城市')
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    StudentNumber = models.IntegerField(verbose_name=u'学习人数',default=0)
    CourseNumber = models.IntegerField(verbose_name=u'课程数',default=0)

    ############################新增机构类别##########################
    Caterory = models.CharField(max_length=20,default='pxjg',verbose_name='机构类别',choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')))
    ##################################################################

    def get_teacher_nums(self):
        #获取教师数量
        return self.teacher_set.all().count()


    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural =verbose_name

    def __str__(self):
        return '{0}'.format(self.Organization)

class Teacher(models.Model):
    BelongOrganization = models.ForeignKey(CourseOrganization,verbose_name=u'所属机构')
    TeacherName = models.CharField(max_length=50,verbose_name=u'教师名称')
    WorkLife = models.IntegerField(verbose_name=u'工作年限',default=0)
    WorkCompany = models.CharField(max_length=50,verbose_name=u'就职公司')
    WorkPosition = models.CharField(max_length=50,verbose_name=u'职位')
    Point = models.CharField(max_length=50,verbose_name=u'教学特点')
    ClickNumber = models.IntegerField(verbose_name=u'点击数', default=0)
    FavoriteNumber = models.IntegerField(verbose_name=u'收藏数', default=0)
    AddTime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    TeacherImage = models.ImageField(upload_to='teacher/%Y/%m',verbose_name=u'教师头像',null=True,blank=True)
    Age = models.IntegerField(verbose_name=u'年龄',default=0,null=True,blank=True)
    Characteristic = models.CharField(max_length=200,verbose_name=u'教学特点',default='',null=True,blank=True)

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural =verbose_name

    def __str__(self):
        return '{0}'.format(self.TeacherName)