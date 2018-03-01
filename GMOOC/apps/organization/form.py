# -*- coding: utf-8 -*-
# @Time    : 2018/1/1 14:47
# @Author  : YeJia_ZhangXin
# @Email   : 345072571@qq.com
# @File    : form.py
# @Software: PyCharm
from django import forms
from operation.models import UserAsk
import re

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['UserName','MobileNumber','CourseName']

    def clean_MobileNumber(self):    #以clean开头，检测字段放在后面
        MobileNumber = self.cleaned_data['MobileNumber']
        REGEXG_MOBILE = '^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])\\d{8}$'
        p = re.compile(REGEXG_MOBILE)
        if p.match(MobileNumber):
            return MobileNumber
        else:
            raise forms.ValidationError(u'手机号码格式不正确',code='mobile_invalid')

