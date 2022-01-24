from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect
from .models import User


# Create your views here.
def login_view(request: HttpRequest):

    if request.method == 'GET':

        # 删除session中存储的user_name和password
        if request.session.get('user_name'):
            del request.session['user_name']
            del request.session['password']
        return render(request, 'user/login.html')

    elif request.method == 'POST':
        # 获取登录中输入的用户名和密码
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=user_name)
        except Exception:
            # 当寻找用户失败 输出报错信息
            return render(request, 'user/login_failed.html', {'error': "用户不存在"})

        if password == user.password:
            # 登录成功之后 修改或新增两个session字段储存登录的用户名和密码
            request.session['user_name'] = user_name
            request.session['password'] = password

            # 转跳用户界面
            return HttpResponseRedirect(reverse('user_interface'))
        else:
            # 登录密码不正确输出密码错误信息
            return render(request, 'user/login_failed.html', {'error': "密码错误"})


def register_view(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    if request.method == 'POST':
        # 获取注册中输入的用户名和密码
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")

        try:
            user = User(username=user_name, password=password)
            user.save()
        except Exception as e:
            # 当生成用户失败时 输出报错信息
            return render(request, 'user/register_failed.html', {'error': e})

        # 成功后将用户名密码保存到session中
        request.session['user_name'] = user_name
        request.session['password'] = password

        return render(request, 'user/register_success.html')


def user_interface_view(request: HttpRequest):

    # 从session中获取用户名和密码
    user_name = request.session.get('user_name')
    password = request.session.get('password')

    try:
        target_user = User.objects.get(username=user_name)
    except Exception as e:
        return render(request, 'user/login_failed.html', {'error', e})

    """
    登录成功之后
    1. 修改密码功能 ok
    2. 登出功能 ok
    3. 显示用户数据
    """
    # 取出用户的创建时间以及更新时间
    create_time = target_user.create_time
    update_time = target_user.update_time

    return render(request, 'user/user_interface.html', locals())


def change_password(request: HttpRequest):

    # 从session中获取用户名和密码
    user_name = request.session.get('user_name')
    password = request.session.get('password')

    if request.method == 'GET':

        return render(request, 'user/change_password.html', locals())

    elif request.method == 'POST':
        try:

            # 通过post获取用户输入的新密码
            new_password = request.POST.get('password')

            # 通过get方法找到该用户的数据
            target_user = User.objects.get(username=user_name)

            # 更新密码
            target_user.password = new_password
            target_user.save()

        except Exception as e:
            return render(request, 'user/change_password_failed.html', {'error': e})

        # 更新session中的密码
        request.session['password'] = new_password

        return render(request, 'user/change_password_success.html')
