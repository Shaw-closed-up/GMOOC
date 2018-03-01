from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import CityDict,CourseOrganization,Teacher
from courses.models import Course
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password
import time
from utils.email_send import send_email
from apps.users.form import LoginForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
# Create your views here.
from .form import UserAskForm
from django.http import HttpResponse
import json
from operation.models import UserFavorite,UserCourse
from django.db.models import Q



"""
内容过滤功能
"""
############课程机构列表############
class OrganiztionListView(View):
    def get(self,request):
        all_city = CityDict.objects.all()
        all_org = CourseOrganization.objects.all()

        # 通过搜索的keywords对数据进行搜索，在路径中的使用GET方法
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_org = all_org.filter(
                Q(Organization__icontains=keywords) | Q(OrganizationDescribe__icontains=keywords))


        ###############################城市筛选功能###################################
        city_id = request.GET.get('city','')    #过去参数
        if city_id:
            all_org = all_org.filter(City_id = int(city_id))


    ###############################机构筛选功能###################################
        category = request.GET.get('ct', '')  # 过去参数
        if category:
            all_org = all_org.filter(Caterory=category)

    ###############################热门授课机构排序###################################
        hot_orgs = all_org.order_by("-FavoriteNumber")[0:3]  #倒叙排名


    ###############################课程排序###################################
        #需要筛选完成后才能进行排序
        sort = request.GET.get('sort', '')  # 过去参数
        if sort:
            if sort == 'student':   #按学生人数进行排名
                all_org = all_org.order_by('-StudentNumber')    #倒叙排列
            if sort == 'course':   #按学生人数进行排名
                all_org = all_org.order_by('-CourseNumber')     #倒叙排列


###############################分页功能###################################
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_org,5,request=request)
        orgs = p.page(page)
##########################################################################

        org_num = all_org.count()   #最后进行统计
        return render(request, 'org_list.html',{
            'all_city':all_city,
            'all_org':orgs,
            'org_num':org_num,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })


###############################用户添加咨询###################################
class UserAskView(View):
    def post(self,request):
        user_ask_form =  UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)  #直接用于数据库存储
            #return HttpResponse("{'status':'success'}",content_type='application/json')        #注明返回的字符串格式
            return HttpResponse(json.dumps({'status':'success'}), content_type='application/json')  # 注明返回的字符串格式
        else:
            return HttpResponse(json.dumps({'status':'fail','msg':'添加出错啦'}),content_type='application/json')     #返回form的errors信息


class OrganiztionDetailView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        organization = CourseOrganization.objects.get(id=int(org_id))
        #teacher = Teacher.objects.filter(BelongOrganization_id=int(org_id))
        teacher = organization.teacher_set.all()[:1]    #根据model的名字和外键的关联，反向取值
        #course = Course.objects.filter(Organization_id=int(org_id))
        course = organization.course_set.all()[:3]     #根据model的名字和外键的关联，反向取值

        #该页面每点击一次，点击量+1
        organization.ClickNumber+=1
        organization.save()

        ###########是否已收藏#############
        has_fav = False #默认未收藏
        #先判断登录
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(User=request.user.id,FavoriteID=organization.id,FavoriteType=2):
                has_fav = True

        return render(request, 'organization_home.html', {'organization':organization, 'teacher':teacher, 'course':course,'has_fav':has_fav})

class OrganiztionCourseView(View):
    """
    机构课程
    """
    def get(self,request,org_id):
        organization = CourseOrganization.objects.get(id=int(org_id))
        #course = Course.objects.filter(Organization_id=int(org_id))
        course = organization.course_set.all()     #根据model的名字和外键的关联，反向取值
        ###########是否已收藏#############
        has_fav = False #默认未收藏
        #先判断登录
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(User=request.user.id,FavoriteID=organization.id,FavoriteType=2):
                has_fav = True
        return render(request, 'organization_course.html', {'organization':organization,  'course':course,'has_fav':has_fav})

class OrganiztionDescribeView(View):
    """
    机构描述
    """
    def get(self,request,org_id):
        organization = CourseOrganization.objects.get(id=int(org_id))
        ###########是否已收藏#############
        has_fav = False #默认未收藏
        #先判断登录
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(User=request.user.id,FavoriteID=organization.id,FavoriteType=2):
                has_fav = True

        return render(request, 'organization_describe.html', {'organization':organization,'has_fav':has_fav})

class OrganiztionTeacherlView(View):
    """
    机构讲师
    """
    def get(self,request,org_id):
        organization = CourseOrganization.objects.get(id=int(org_id))
        #teacher = Teacher.objects.filter(BelongOrganization_id=int(org_id))
        teacher = organization.teacher_set.all()    #根据model的名字和外键的关联，反向取值
        ###########是否已收藏#############
        has_fav = False #默认未收藏
        #先判断登录
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(User=request.user.id,FavoriteID=organization.id,FavoriteType=2):
                has_fav = True
        return render(request, 'organization_teacher.html', {'organization':organization, 'teacher':teacher,'has_fav':has_fav})

class AddFavView(View):
    """
    添加收藏和取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)  #获取收藏的id，根据收藏类型进行判断，可能是课程，可能是机构，可能是老师，避免错误，不要post空串，因为空串进行int转换的时候会报错，“0”表示默认信息
        fav_type = request.POST.get('fav_type',0)

        #进行收藏前，先判断用户是否登陆
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status':'fail','msg':'用户未登录'}),content_type='application/json')     #返回form的errors信息，跳转在Ajax中完成

        #实现用户收藏和取消收藏功能，利用user,fav_id,fav_type进行过滤，获取用户UserFavorite信息，注意变量类型要与model一致
        exit_records = UserFavorite.objects.filter(User=request.user.id,FavoriteID=int(fav_id),FavoriteType=int(fav_type))
        if exit_records:
            #记录已经存在，则表面用户像取消收藏
            exit_records.delete()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}),content_type='application/json')  # 返回form的errors信息，跳转在Ajax中完成

        else:
            #若查询不到该条收藏记录，则表面用户想进行收藏，进行数据存储逻辑
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.FavoriteID = int(fav_id)
                user_fav.FavoriteType = int(fav_type)
                user_fav.User = request.user       #切记外键一定要传进来
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}),content_type='application/json')  # 返回form的errors信息，跳转在Ajax中完成
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错'}),content_type='application/json')  # 返回form的errors信息，跳转在Ajax中完成


class TeacherListView(View):
    def get(self,request):
        #获取所有教师信息
        all_teacher = Teacher.objects.all()
        #获取热门教师信息
        hot_teachers = Teacher.objects.all().order_by('ClickNumber')[:3]
        #教师人数
        teachers_num = all_teacher.count()

        #通过搜索的keywords对数据进行搜索，在路径中的使用GET方法
        keywords = request.GET.get('keywords','')
        if keywords:
            all_teacher = all_teacher.filter(Q(TeacherName__icontains=keywords)|Q(WorkCompany__icontains=keywords)|Q(WorkCompany__icontains=keywords)|Q(Characteristic__icontains=keywords))

        ###############################课程排序###################################
        # 需要筛选完成后才能进行排序
        sort = request.GET.get('sort', '')  # 过去参数
        if sort:
            if sort == 'hot':  # 按学生人数进行排名
                all_teacher = all_teacher.order_by('-ClickNumber')  # 倒叙排列

        ###############################分页功能###################################
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teacher, 2, request=request)
        teachers = p.page(page)
        return render(request, 'teachers_list.html', {'teachers':teachers,'hot_teachers':hot_teachers,'sort':sort,'teacher_num':teachers_num})



class TeacherDetailView(View):
    def get(self,request,teacher_id):
        #教师信息
        teacher = Teacher.objects.get(id=teacher_id)
        #教师的课程
        courses = teacher.course_set.all()[:3]  #course内有teacher这个外键，利用_set获取与该teacher相关的所有课程
        #教师排行榜
        all_teacher = Teacher.objects.all()
        #收藏状态
        teacher_fav = False

        #该页面每点击一次，点击量+1
        teacher.ClickNumber+=1
        teacher.save()

        organization_fav = False
        if  request.user.is_authenticated():    #先判断是否登陆
            if UserFavorite.objects.filter(User=request.user.id,FavoriteID=teacher.id,FavoriteType=3):
                teacher_fav = True
            if UserFavorite.objects.filter(User=request.user.id, FavoriteID=teacher.id, FavoriteType=2):
                organization_fav = True
        return render(request, 'teacher_detail.html', {'teacher':teacher,'courses':courses,'all_teacher':all_teacher,'teacher_fav':teacher_fav,'organization_fav':organization_fav})


class TeacherDetailTestView(View):
    def get(self,request,teacher_id):
        return render(request, 'teacher-detail-test.html', {})


