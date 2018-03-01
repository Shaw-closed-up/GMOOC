# -*- coding: utf-8 -*-
# @Time    : 2017/12/10 15:00
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : form.py
# @Software: PyCharm

from django import forms
from captcha.fields import CaptchaField
from users.models import UserProfile
import re

class LoginForm(forms.Form):
    #字段名称一定要对应
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})

class ForgetpwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})

class PasswordResetForm(forms.Form):
    password = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)

class UserImgUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['img']

class UserInfodForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','adress','mobile']

    def clean_MobileNumber(self):    #以clean开头，检测字段放在后面
        MobileNumber = self.cleaned_data['mobile']
        REGEXG_MOBILE = '^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])\\d{8}$'
        p = re.compile(REGEXG_MOBILE)
        if p.match(MobileNumber):
            return MobileNumber
        else:
            raise forms.ValidationError(u'手机号码格式不正确',code='mobile_invalid')
