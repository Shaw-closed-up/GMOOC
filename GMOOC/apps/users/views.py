from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyCode
from django.views.generic.base import View
from django.http import HttpResponseRedirect,HttpResponse    #重定向
#用于数学运算
from django.db.models import Q
from .form import LoginForm,RegisterForm,ForgetpwdForm,PasswordResetForm,UserImgUploadForm,UserInfodForm
from django.contrib.auth.hashers import make_password
import time
from utils.email_send import send_email
import json
from operation.models import UserCourse,UserFavorite,UserMessage
from courses.models import Course
from organization.models import Teacher,CourseOrganization
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Banner
from django.core.urlresolvers import reverse

# Create your views here.



#重写authenticate方法,在setting中配置该方法，后台自动调用
#继承ModelBackend方法，实现后台自动调用
#相当于重构了authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self,username=None,password=None,**kwargs):
        try:
            #查询值,数据库中的查询值若有相同则返回null
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))    #查询服务器，对服务器有一定压力
            #密码认证
            if user.check_password(password):
                 return user
        except Exception as e:
            return None

###############基于类的login函数#######################
class LoginView(View):
    def get(self,request):

        ##################加入重定向至来时页面函数#################
        # 已经在来时页面埋点，将来时页面埋点在参数next中
        next_page = request.GET.get('next', '')
        ###########################################################

        return render(request,'login.html',{'next_page':next_page})  #将next_page返回给html页面，进行埋点传值给POST
    def post(self,request):
        login_form = LoginForm(request.POST)
        #返回报错值，有报错则valid为False，没报错则为True，减少服务器查询压力。
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 使用authenticate对用户正确性进行简单判断，判断正确返回user 的对象，如果错误返回None
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                #增加判断用户是否激活（可能只注册但未激活）
                if user.is_active:
                    # 调用login函数，实现对request进行操作，将用户信息、session、cookies等写入了request中，再用render将request进行返回
                    login(request, user)
                    #################传用户信息进登陆页面#################
                    LoginMsg = UserProfile.objects.get(username=user_name)

                    #################获取html中的隐藏字段next_page#################
                    next_page = request.POST.get('next_page','')
                    if next_page == '':
                        return HttpResponseRedirect('/')  # 转到index页面
                        #return HttpResponseRedirect(reverse("index"))  # 转到index页面

                    else:
                        return HttpResponseRedirect(next_page)  # 转到来时页面
                    #return render(request, 'index.html', {'LoginMsg':LoginMsg})    #登陆成功，由后台渲染跳转至index，并在index中判断，头部显示
                else:
                    return render(request, 'login.html', {'msg':'用户未完成激活'})
            else:
                # 通过了form表单的验证，但是账号密码不正确时
                return render(request, 'login.html', {"msg": "账号密码有问题"})
        else:
            # form表单验证不通过，返回表单错误信息
            return render(request, 'login.html', {"login_form": login_form})    #直接传入login_form，在Template里面调用error值

#新增注销功能函数
def logout_view(request):
    if request.method == 'GET':
        next_page = request.GET.get('next', '/')
    logout(request)
    return HttpResponseRedirect(next_page)  # 转到来时页面
    #return render(request, 'index.html', {})  # 登陆成功，由后台渲染跳转至index，并在index中判断，头部显示


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})  #将register_form数据传递给Template
        #return render(request,'register.html',{})
    def post(self, request):
        register_form = RegisterForm(request.POST)  #将post上来的数据传递给RegisterForm
        if register_form.is_valid():    #上传的数据符合form表要求，有效
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form,'msg': '用户已存在'})  # 该逻辑用户判断用户是否已注册存在
            pass_word = request.POST.get('password','')
            ########注册的时候需要查看邮箱是否有重复,利用了username进行了去重#######
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            #明文数据需要经过加密后传入数据库,利用make_password方法加密
            user_profile.password = make_password(pass_word)
            user_profile.is_active = 0  #表面用户还未激活
            user_profile.save()
            #用于邮件激活操作
            send_email(user_name, send_type='register')
            return render(request, 'login.html', {})  # 将register_form数据传递给Template
        else:
            #注册失败跳转至register页面，暂时
            #return render(request,'index.html',{})
            return render(request, 'register.html', {'register_form':register_form})  # 将register_form数据传递给Template



class ActiveUserView(View):
    def get(self,request,active_code): #利用code在EmailVerifyCode进行查询
        EmailVerifyCodeRecorder = EmailVerifyCode.objects.filter(code=active_code)
        if EmailVerifyCodeRecorder:
            #找到UserProfile中的对应账号，并设is_active为1,即为激活账号
            for i in EmailVerifyCodeRecorder:
                email = i.email
                user = UserProfile.objects.get(email=email)
                user.is_active = 1
                return render(request, 'login.html', {})
        else:
            return render(request, 'active_fail.html', {})  #找不到记录则返回连接失效的页面


class ForgetpwdView(View):
    def get(self,request):
        forgetpwd_form = ForgetpwdForm()
        return render(request,'forgetpwd.html',{'forgetpwd_form':forgetpwd_form})    #将验证码传递给前端
    def post(self,request):
        forgetpwd_form = ForgetpwdForm(request.POST)
        if forgetpwd_form.is_valid():
            #post数据成功，将验证码保存在EmailVerifyCode，用于激活查询，并跳转至index页面
            email = request.POST.get('email')
            send_email(email, send_type='find_password')
            return render(request,'send_success.html',{})
        else:
            #验证码错误或邮箱格式错误返回信息
            return render(request,'forgetpwd.html',{'forgetpwd_form':forgetpwd_form})


class PasswordReset(View):
    def get(self,request,active_code):
        return render(request,'password_reset.html',{}) #获取修改密码页面

    def post(self,request,active_code):
        EmailVerifyCodeRecorder = EmailVerifyCode.objects.filter(code=active_code)  #通过active_code去EmailVerifyCode找到对应的email
        if EmailVerifyCodeRecorder: #如果该验证码存在
            # 找到UserProfile中的对应账号，进行修改密码
            for i in EmailVerifyCodeRecorder:   #一般来说该验证码是唯一的
                email = i.email #找到email
                user = UserProfile.objects.get(email=email) #通过email在UserProfile中找到对应的用户数据
                password_reset = PasswordResetForm(request.POST)    #新密码上传至表单中
                if password_reset.is_valid():   #新设置的密码符合表单的话
                    password = request.POST.get('password','')
                    password2 = request.POST.get('password2','')
                    if password == password2: #两个密码相同，所有逻辑正确，进行密码修改
                        #在数据库中信息密码修改
                        user.password = make_password(password)
                        user.save()
                        return render(request, 'login.html', {})  # 将register_form数据传递给Template
                    else:   #如果两个密码不相同
                        return render(request, 'password_reset.html', {'msg':'两个密码不一致'})  # 将register_form数据传递给Template
                else:   #表单验证不通过
                    return render(request, 'password_reset.html', {'msg':'密码未填写或格式有问题'})
        else:
                pass    #返回404页面


                ###############基于函数的login函数#######################
# def user_login(request):
#     #判断前段进来的是get还是post方法，get返回登陆页面，post方法表示提交了数据，需要后台对用户账号密码是否正确做判断
#     if request.method == "POST":
#         #加入后台逻辑，对用户登陆进行判断
#         #get函数后面的''是默认值
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#
#         #使用authenticate对用户正确性进行简单判断，判断正确返回user 的对象，如果错误返回None
#         user = authenticate(username = user_name,password = pass_word)
#         if user is not None:
#             #调用login函数，实现对request进行操作，将用户信息、session、cookies等写入了request中，再用render将request进行返回
#             login(request,user)
#             return render(request, 'index.html', {})
#         else:
#             #账号密码有问题时
#             return render(request, 'login.html', {"msg":"账号密码有问题"})
#     #如果前段获取的还是get方法则返回登陆页面
#     elif request.method == "GET":
#         return render(request,'login.html',{})

class UserInfoView(View):
    def get(self,request):
        next_page = request.path   #获取来时路径
        #判断是否登陆
        if not request.user.is_authenticated():
            #return render(request,'usercenter_info.html',{})
            target_url = '/login/?next='+next_page      #拼凑成与login对应的url
            return HttpResponseRedirect(target_url)  # 转到来时页面
        if request.user.is_authenticated():
            return render(request,'usercenter_info.html',{})

    def post(self,request): #注意form表单需要加入csrf-tpken
        user_info_form = UserInfodForm(request.POST)
        if user_info_form.is_valid():
            request.user.nick_name = request.POST.get('nick_name')
            request.user.birthday = request.POST.get('birthday')
            request.user.gender = request.POST.get('gender')
            request.user.adress = request.POST.get('adress')
            request.user.mobile = request.POST.get('mobile')
            request.user.save()
            return HttpResponse(json.dumps({'status': 'success'}),content_type='application/json')  # 将register_form数据传递给Template
        else:
            return HttpResponse(json.dumps({'status': 'failure','msg':user_info_form.errors}),content_type='application/json')  # 将register_form数据传递给Template


class UserImgUploadView(View):
    def post(self,request): #上传是用post方法
        next_page = request.path   #获取来时路径
        #判断是否登陆
        if not request.user.is_authenticated():
            target_url = '/login/?next='+next_page      #拼凑成与login对应的url
            return HttpResponseRedirect(target_url)  # 转到来时页面
        if request.user.is_authenticated():
            #可以进行图片上传工作
            img_upload_form = UserImgUploadForm(request.POST,request.FILES)
            if img_upload_form.is_valid():
                #验证通过后会将上传图片放在cleaned_data内
                image = img_upload_form.files['image']      #尝试直接从files里面取值
                #对获取的图片进行保存
                request.user.img = image
                request.user.save()

class UserPasswordUpdateView(View):
    def post(self,request):
        password_reset_form = PasswordResetForm(request.POST)    #新密码上传至表单中
        if password_reset_form.is_valid():   #新设置的密码符合表单的话
            password = request.POST.get('password','')
            password2 = request.POST.get('password2','')
            if password == password2: #两个密码相同，所有逻辑正确，进行密码修改
                #在数据库中信息密码修改
                request.user.password = make_password(password)
                request.user.save()
                return HttpResponse(json.dumps({'status': 'success'}),content_type='application/json')  # 将register_form数据传递给Template
                #return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')  # 注明返回的字符串格式
            else:   #如果两个密码不相同
                return HttpResponse(json.dumps({'status': 'fail','msg':'两个密码不同'}), content_type='application/json')  # 将register_form数据传递给Template
        else:   #表单验证不通过
            return HttpResponse(json.dumps({'status': 'fail', 'msg': password_reset_form.errors}),content_type='application/json')  # 将register_form数据传递给Template

#发送更新邮箱验证码
class EmailCodeView(View):
    def get(self,request):
        #判断是否登陆，如果未登陆则回到login页面
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')  # 转到来时页面
        else:
            email = request.GET.get('email','')
            # 查询该邮箱是否已经存在，如果有人已经用了该邮箱则不可以继续用
            whether_exit_email = UserProfile.objects.filter(email=email)
            if whether_exit_email:
                #告诉用户该邮箱已经存在
                return HttpResponse(json.dumps({'email': '邮箱已经存在'}), content_type='application/json')  # 将register_form数据传递给Template
            else:
                #邮箱不存在为可用邮箱，则发送邮箱验证码，并在EmailVerifyCode进行存储数据
                send_email(email, send_type='update')   #发送验证码
                return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')  # 将register_form数据传递给Template

#邮箱更新view
class UpdateEmailView(View):
    def post(self,request):
        # 判断是否登陆，如果未登陆则回到login页面
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')  # 转到来时页面
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        # 查询该邮箱及验证码信息
        exit_email = EmailVerifyCode.objects.filter(email=email,code=code)
        if exit_email:  #有该条记录则验证正确可以进行修改，完成验证码验证功能，可以进行邮箱修改
            request.user.email = email
            request.user.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')



class MyCourseView(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')  # 转到来时页面
        user_id = request.user.id
        my_courses = UserCourse.objects.filter(User_id=user_id)
        return render(request,'usercenter_mycourse.html',{'my_courses':my_courses})


class MyFavView(View):
    def get(self,request):
        choice = request.GET.get('choice')
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')  # 转到来时页面
        user_id = request.user.id
        my_fav = UserFavorite.objects.filter(User_id=user_id)
        fav_course_id = my_fav.filter(FavoriteType=1)
        fav_organization_id = my_fav.filter(FavoriteType=2)
        fav_teacher_id = my_fav.filter(FavoriteType=3)

        #加入筛选逻辑
        fav = []
        #获取所有收藏课程
        if choice == 'course':
            for i in fav_course_id:
                course = Course.objects.get(id=i.FavoriteID)
                fav.append(course)

        #获取所有收藏组织
        if choice == 'organization':
            for i in fav_organization_id:
                fav.append(CourseOrganization.objects.get(id=i.FavoriteID))

        #获取所有收藏老师
        if choice == 'teacher':
            for i in fav_teacher_id:
                fav.append(Teacher.objects.get(id=i.FavoriteID))

        return render(request,'usercenter_fav.html',{'fav':fav,'choice':choice})

class MyMessageView(View):
    def get(self,request):
        messages = UserMessage.objects.filter(User=request.user.id)
        #分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(messages,1,request=request)
        messages = p.page(page)

        return render(request,'usercenter_message.html',{'messages':messages})


class IndexView(View):
    def get(self,request):
        banners = Banner.objects.all()
        courses_banner = Course.objects.filter(Display=True)
        courses = Course.objects.filter(Display=False)[:6]
        organization = CourseOrganization.objects.all()[:20]
        return render(request, 'index.html', {'banners':banners,'courses_banner':courses_banner,'courses':courses,'organization':organization})


#404页面
def page_not_found(request):
    return render(request, '404.html')

#500页面
def page_error(request):
    return render(request, '500.html')

#403页面
def permission_denied(request):
    return render(request, '403.html')