# utf-8

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from vote.models import Subject, Teacher, User
from vote.form import RegisterForm, LoginForm
from vote.captcha import Captcha
from vote.utils import generate_captcha_code
import random
import xlwt
from io import BytesIO
from urllib.parse import quote
from vote.mapper import SubjectMapper

# Create your views here.

# def show_subjects(request):
#     """查看所有学科"""
#     subjects = Subject.objects.all()
#     return render(request, 'subject.html', {'subjects': subjects})

# 前后端分离
def show_subjects(request):
    """查看所有学科"""
    queryset = Subject.objects.all()
    subjects = []
    # for subject in queryset:
    #     subjects.append({
    #         'no': subject.no,
    #         'name': subject.name,
    #         'intro': subject.intro,
    #         'isHot': subject.is_hot
    #     })

    for subject in queryset:
        subjects.append(SubjectMapper(subject).as_dict())

    return JsonResponse(subjects, safe=False)

def show_teachers(request):
    """显示指定学科的老师"""
    try:
        sno = int(request.GET['sno'])
        subject = Subject.objects.get(no=sno)
        teachers = subject.teacher_set.all()
        return render(request, 'teachers.html', {'subject': subject, 'teachers': teachers})
    except (KeyError, ValueError, request.DoesNotExist):
        return reversed('/')

def praise_or_criticize(request):
    """好评"""
    if 'username' in request.session:
        try:
            tno = int(request.GET['tno'])
            teacher = Teacher.objects.get(no=tno)
            if request.path.startswith('/praise'):
                teacher.good_count += 1
            else:
                teacher.bad_count += 1
            teacher.save()
            data = {'code': 200, 'hint': '操作成功'}
        except (KeyError, ValueError, Teacher.DoseNotExist):
            data = {'code': 404, 'hint': '操作失败'}
    else:
        data = {'code': 401, 'hint': '请先登录'}

    return JsonResponse(data)

def register(request):
    page, hint = 'register.html', ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print('----', form)
        if form.is_valid():
            form.save()
            page = 'login.html'
            hint = '注册成功，请登录'
        else:
            hint = '请输入有效的注册信息'
    return render(request, page, {'hint': hint})

def login(request):
    hint = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
             # 对验证码的正确性进行验证
            captcha_from_user = form.cleaned_data['captcha']
            captcha_from_sess = request.session.get('captcha', '')
            if captcha_from_sess.lower() != captcha_from_user.lower():
                hint = '请输入正确的验证码'
            else:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.filter(username=username, password=password).first()
                if user:
                    # 登录成功后将用户编号和用户名保存在session中
                    request.session['userid'] = user.no
                    request.session['username'] = user.username
                    return redirect('/')
                else:
                    hint = '用户名或密码错误'
        else:
            hint = '请输入有效的登录信息'
    return render(request, 'login.html', {'hint': hint})

def logout(request):
    """注销"""
    request.session.flush()
    return redirect('/')

def get_captcha(request):
    code = generate_captcha_code()
    request.session['captcha'] = code
    image_data = Captcha.instance().generate(code, fmt='PNG')
    return HttpResponse(image_data, content_type='image/png')

def export_teachers_excel(request):
    # 创建工作簿
    wb = xlwt.Workbook()
    # 添加工作表
    sheet = wb.add_sheet('老师信息表')
    # 查询所有老师的信息(注意：这个地方稍后需要优化)
    # queryset = Teacher.objects.all()
    queryset = Teacher.objects.all().select_related('subject')
    # 向Excel表单中写入表头
    colnames = ('姓名', '介绍', '好评数', '差评数', '学科')
    for index, name in enumerate(colnames):
        sheet.write(0, index, name)
    # 向单元格中写入老师的数据
    props = ('name', 'detail', 'good_count', 'bad_count', 'subject')
    for row, teacher in enumerate(queryset):
        for col, prop in enumerate(props):
            value = getattr(teacher, prop, '')
            if isinstance(value, Subject):
                value = value.name
            sheet.write(row + 1, col, value)
    # 保存Excel
    buffer = BytesIO()
    wb.save(buffer)
    # 将二进制数据写入响应的消息体中并设置MIME类型
    resp = HttpResponse(buffer.getvalue(), content_type='application/vnd.ms-excel')
    # 中文文件名需要处理成百分号编码
    filename = quote('老师.xls')
    # 通过响应头告知浏览器下载该文件以及对应的文件名
    resp['content-disposition'] = 'attachment; filename="%s"' % filename
    return resp
    
def get_teachers_data(request):
    # 查询所有老师的信息(注意：这个地方稍后也需要优化)
    queryset = Teacher.objects.all()
    # 用生成式将老师的名字放在一个列表中
    names = [teacher.name for teacher in queryset]
    # 用生成式将老师的好评数放在一个列表中
    good = [teacher.good_count for teacher in queryset]
    # 用生成式将老师的差评数放在一个列表中
    bad = [teacher.bad_count for teacher in queryset]
    # 返回JSON格式的数据
    return JsonResponse({'names': names, 'good': good, 'bad': bad})