from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect
from .models import User
import hashlib


# useful method
def password_is_correct(password, user: User):
    """
    检查密码输入是否正确
    :param password: 输入的密码
    :param user: 用户数据词条
    :return: True - 密码正确
            False - 密码错误
    """
    # 用MD5将用户输入的密码进行加密
    m = hashlib.md5()
    m.update(password.encode())
    password_after_hash = m.hexdigest()

    if password_after_hash == user.password:
        return True
    else:
        return False


# Create your views here.
def login_view(request: HttpRequest):

    if request.method == 'GET':

        # 删除session中存储的user_name和uid
        if request.session.get('user_name'):
            del request.session['user_name']
            del request.session['uid']
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

        if password_is_correct(password, user):
            # 登录成功之后 修改或新增两个session字段储存登录的用户名和密码
            request.session['user_name'] = user_name
            request.session['uid'] = user.id

            # 转跳用户界面
            return HttpResponseRedirect(reverse('user_interface'))
        else:
            # 登录密码不正确输出密码错误信息
            return render(request, 'user/login_failed.html', {'error': "密码错误"})


def register_view(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    if request.method == 'POST':
        # 获取注册中输入的用户名和密码以及确认密码
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        password_check = request.POST.get("password_check")

        # 首先确保 密码确认成功
        if password != password_check:
            return render(request, 'user/register_failed.html', {'error': '两次密码输入不相同'})

        """
        使用哈希算法对用户的输入的密码进行加密 以便存储入数据库后防止密码泄露
        常用的哈希算法有md5 sha-256等 计算较快的是md5 常常用来记录密码
        特点:
        1. 定长输出：不管明文多长 加密过后的密文长度一定 md5 - 32位16进制
        2. 不可逆：无法逆向获得明文
        3. 使用场景：
            1, 密码加密
            2, 文件完整性校验
        4. 使用方法：
            1. import hashlib
            2. m = hashlib.md5()
            3. m.update(明文 必须是字节串) 字节串比如：b'123456' eg. m.update(b'123456')
                将普通字符串变成字节串可以使用 字符串.encode() 或者 b'字符串内容'
                update是累加 也就是说之后对m的update会把新的字符累加到之前明文之后
            4. result = m.hexdigest() 使用十六进制的方式进行消化并得到结果
        """

        # 用MD5将用户输入的密码进行加密
        m = hashlib.md5()
        m.update(password.encode())
        password_after_hash = m.hexdigest()

        try:
            user = User(username=user_name, password=password_after_hash)
            user.save()
        except Exception as e:
            print('--create user error-- Detail: {}'.format(e))
            # 当生成用户失败时 输出报错信息
            return render(request, 'user/register_failed.html', {'error': '用户名已被注册'})

        # 成功后将用户名以及用户id保存到session中
        request.session['user_name'] = user_name
        request.session['uid'] = user.id

        return render(request, 'user/register_success.html')


def user_interface_view(request: HttpRequest):

    # 从session中获取用户名id
    uid = request.session.get('uid')
    # 如果为空需要转跳登录界面
    if uid:
        user_name = request.session.get('user_name')
    else:
        return HttpResponseRedirect(reverse('user_login'))

    try:
        target_user = User.objects.get(id=uid)
    except Exception as e:
        # 产生错误时倒回登录失败界面 （除非session被修改，不然不会产生错误）
        return render(request, 'user/login_failed.html', {'error': e})

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

    # 从session中获取用户名id
    uid = request.session.get('uid')
    # 如果为空需要转跳登录界面
    if uid:
        user_name = request.session.get('user_name')
    else:
        return HttpResponseRedirect(reverse('user_login'))

    if request.method == 'GET':

        return render(request, 'user/change_password.html', locals())

    elif request.method == 'POST':
        # 获取用户数据
        try:
            # 通过get方法找到该用户的数据
            target_user = User.objects.get(id=uid)
        except Exception as e:
            print(e)
            return render(request, 'user/change_password_failed.html', {'error': '用户不存在'})

        # 通过post获取用户输入的旧密码、新密码以及确认密码
        origin_password = request.POST.get('origin_password')
        new_password = request.POST.get('new_password')
        password_check = request.POST.get('password_check')

        # 先检查密码确认
        if password_check != new_password:
            return render(request, 'user/change_password_failed.html', {'error': '两次密码输入不相同'})

        # 再判断 旧密码是否正确
        if not password_is_correct(origin_password, target_user):
            return render(request, 'user/change_password_failed.html', {'error': '密码输入错误'})

        # 用MD5将用户输入的密码进行加密
        m = hashlib.md5()
        m.update(new_password.encode())
        password_after_hash = m.hexdigest()

        # 更新密码
        try:
            target_user.password = password_after_hash
            target_user.save()
        except Exception as e:
            print(e)
            return render(request, 'user/change_password_failed.html', {'error': e})

        return render(request, 'user/change_password_success.html')



