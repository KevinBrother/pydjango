from django import forms
from django.forms import ValidationError
from vote.models import User

import re
import hashlib


USERNAME_PATTERN = re.compile(r'\w{4,40}')

class RegisterForm(forms.ModelForm):
    repassword = forms.CharField(min_length=8, max_length=40)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not USERNAME_PATTERN.fullmatch(username):
            raise ValidationError('用户名由字母、数字和下划线构成且长度为4-40个字符')
        return username
        
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 or len(password) > 40:
            raise ValidationError('无效的密码，密码长度为8-40个字符')
        return to_md5_hex(self.cleaned_data['password'])

    def clean_repassword(self):
        repassword = to_md5_hex(self.cleaned_data['repassword'])
        if repassword != self.cleaned_data['password']:
            raise ValidationError('密码和确认密码不一致')
        return repassword

    class Meta:
        model = User
        exclude = ('no', 'regdate')


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=8, max_length=30)
    # captcha = forms.CharField(min_length=4, max_length=4)
    captcha = forms.CharField(max_length=4)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not USERNAME_PATTERN.fullmatch(username):
            raise ValidationError('无效的用户名')
        return username

    def clean_password(self):
        return to_md5_hex(self.cleaned_data['password'])


def to_md5_hex(message):
    return hashlib.md5(message.encode()).hexdigest()