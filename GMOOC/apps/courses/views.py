from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password
import time
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from .models import Course,Lesson,Video,CourseResource
from operation.models import UserCourse,CourseComment



class CoursesListView(View):
    def get(self,request):
        ###############################筛选功能###################################
        sort = request.GET.get('sort', '')
        if sort == 'last':
            all_course = Course.objects.all().order_by('-AddTime')
        elif sort == 'hot':
            all_course = Course.objects.all().order_by('-Students')
        elif sort == 'student':
            all_course = Course.objects.all().order_by('-ClikeNumber')
        else:
            all_course = Course.objects.all()

        # 通过搜索的keywords对数据进行搜索，在路径中的使用GET方法
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_course = all_course.filter(Q(CourseName__icontains=keywords) | Q(Describe__icontains=keywords)|Q(Detail__icontains=keywords)|Q(CourseType__icontains=keywords))


                ###############################分页功能###################################
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_course,9, request=request)
        course = p.page(page)
            ###########################热门课程推荐################################
        hot_course = Course.objects.all().order_by('-FavouriteNumber')[:3]

        return render(request, 'course_list.html',{'all_course':course,'sort':sort,'hot_course':hot_course})


class CourseDetailView(View):
    def get(self,request,course_id):
        course_detail = Course.objects.get(id=course_id)
        #每次单击进入课程详情页面都会触发一次点击数
        course_detail.ClikeNumber+=1
        course_detail.save()
        #查询所有tag，获取推荐课程
        tag = course_detail.Tag
        if tag: #如果有打标签
            relate_course = Course.objects.filter(Tag=tag).filter(~Q(id= int(course_id)))[:1]
        # else:
        #     relate_course = []  #怎么都要传回一个数组，如果传回模板是空的话，会取不到值，会报错
        return render(request, 'course_detail.html',{'course_detail':course_detail,'relate_course':relate_course})

class CourseVideoView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        lesson = Lesson.objects.filter(Course=course)
        course_resource = CourseResource.objects.filter(Course=course)
        ##########################学过该课程的同学还学过##########################
        #利用opreation-UserCourse记录的用户行为，在用户选择学习后，需要将用户行为存储进入该数据库中

        Other_User_List = UserCourse.objects.filter(Course=course)  #利用课程数据遍历出所有学习该课程下的用户
        Related_Courses = set()
        Related_Courses_id = set()
        for u in Other_User_List:
            user_courses = UserCourse.objects.filter(User_id=u.id)    #遍历所有用户，并利用用户id遍历出所有的course,注意起名字不要重复了
            for c in user_courses:
                if c.Course_id not in Related_Courses_id:   #利用课程id进行去重
                    Related_Courses.add(c)
                    Related_Courses_id.add(c.Course_id)

        ##########################实现用户学习行为的记录#################################
        user = request.user
        exit_recorder = UserCourse.objects.filter(User=user,Course=course)
        if not exit_recorder:
            user_cour = UserCourse()
            user_cour.Course = course
            user_cour.User = user
            user_cour.save()
        ##################################################################################
        return render(request, 'course_video.html',{'course':course,'lesson':lesson,'course_resource':course_resource,'Related_Courses':Related_Courses,})


class CourseCommentView(View):
    #评论数据展示
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        course_comment = CourseComment.objects.filter(Course=course) #遍历所有课程的评论
        course_resource = CourseResource.objects.filter(Course=course)
        ##########################学过该课程的同学还学过##########################
        # 利用opreation-UserCourse记录的用户行为，在用户选择学习后，需要将用户行为存储进入该数据库中
        Other_User_List = UserCourse.objects.filter(Course=course)  # 利用课程数据遍历出所有学习该课程下的用户
        Related_Courses = set()
        Related_Courses_id = set()
        for u in Other_User_List:
            user_courses = UserCourse.objects.filter(User_id=u.id)  # 遍历所有用户，并利用用户id遍历出所有的course,注意起名字不要重复了
            for c in user_courses:
                if c.Course_id not in Related_Courses_id:  # 利用课程id进行去重
                    Related_Courses.add(c)
                    Related_Courses_id.add(c.Course_id)
        ##########################################################################
        return render(request, 'course_comment.html',{'course': course,'Related_Courses': Related_Courses,'course_comment':course_comment,'course_resource':course_resource})


class CourseAddCommentView(View):
    def post(self,request):
        #首先判断是否登陆
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status':'fail','msg':'用户未登录'}),content_type='application/json')     #返回form的errors信息，跳转在Ajax中完成
        course_id = request.POST.get('course_id',0)
        user = request.user
        comment = request.POST.get('comments',0)
        if int(course_id)>0 and comment:
            course_comment = CourseComment()
            course = Course.objects.get(id=course_id)
            course_comment.Course = course
            course_comment.User = user
            course_comment.Comment = comment
            course_comment.save()
            return HttpResponse(json.dumps({'status':'success','msg':'评论成功'}),content_type='application/json')     #返回form的errors信息，跳转在Ajax中完成


class VideoPlayView(View):
    def get(self,request,video_id):
        return render(request, 'video_play.html',{})

