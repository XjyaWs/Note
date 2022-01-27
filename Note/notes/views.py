from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from .models import Note
from user.models import User


# Useful method
def check_login(request: HttpRequest):
    """
    检验发来的request是否带有已登录的session或者Cookie
    :param request
    :return: 登录状态 False-未登录 True-登录 用户id 用户名
    """
    # 从session中获取用户id
    uid = request.session.get('uid')
    # 如果为空需要转跳登录界面
    if uid:
        user_name = request.session.get('user_name')
    else:
        # 再检查cookies
        # 从cookies中获取用户名id
        uid = request.COOKIES.get("uid")
        if uid:
            user_name = request.COOKIES.get("user_name")
            # 将数据复写入session中
            request.session['uid'] = uid
            request.session['user_name'] = user_name
        else:
            return False, None, None

    return True, uid, user_name


# Create your views here.
def new_note_view(request: HttpRequest):

    # 进行登录检查
    login_flag, uid, user_name = check_login(request)

    # 如果没有登录
    if not login_flag:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "GET":
        return render(request, 'notes/new_note.html')

    elif request.method == "POST":
        # 获取post中的标题以及笔记内容信息
        title = request.POST.get("title")
        content = request.POST.get("content")

        # 获取该用户
        try:
            user = User.objects.get(id=uid)
        except Exception as e:
            print('--create note error-- {}'.format(e))
            return HttpResponse('添加新笔记失败 原因：{}'.format(e))

        # 添加新note
        new_note = Note(title=title, content=content, user=user)

        try:
            new_note.save()
        except Exception as e:
            print('--create note error-- {}'.format(e))
            return HttpResponse('添加新笔记失败 原因：{}'.format(e))

        return HttpResponse('--add new note success--')


def note_detail_view(request: HttpRequest, id):

    # 进行登录检查
    login_flag, uid, user_name = check_login(request)

    # 如果没有登录
    if not login_flag:
        return HttpResponseRedirect(reverse('index'))

    try:
        target_note = Note.objects.get(id=id, is_active=True)
    except Exception as e:
        print('--note detail error-- {}'.format(e))
        return HttpResponseNotFound()

    # 当用户id和文章id无法对应的时候返还404错误
    if uid == target_note.user.id:
        return render(request, 'notes/note_detail.html', locals())
    else:
        return HttpResponseNotFound()


def update_note_view(request: HttpRequest, id):

    # 进行登录检查
    login_flag, uid, user_name = check_login(request)

    # 如果没有登录
    if not login_flag:
        return HttpResponseRedirect(reverse('index'))

    try:
        target_note = Note.objects.get(id=id, is_active=True)
    except Exception as e:
        print('--update note error-- {}'.format(e))
        return HttpResponseNotFound()

    # 当用户id和文章id无法对应的时候返还404错误
    if uid != target_note.user.id:
        return HttpResponseNotFound()

    # 主任务逻辑
    if request.method == "GET":
        return render(request, 'notes/update_note.html', locals())

    elif request.method == "POST":
        # 获取post中的标题以及笔记内容信息
        title = request.POST.get("title")
        content = request.POST.get("content")

        # 更新note
        target_note.title = title
        target_note.content = content

        try:
            target_note.save()
        except Exception as e:
            print('--update note error-- {}'.format(e))
            return HttpResponse('更新笔记失败 原因：{}'.format(e))

        return HttpResponse('--update note success!--')


def delete_note_view(request: HttpResponse, id):

    # 进行登录检查
    login_flag, uid, user_name = check_login(request)

    # 如果没有登录
    if not login_flag:
        return HttpResponseRedirect(reverse('index'))

    try:
        target_note = Note.objects.get(id=id, is_active=True)
    except Exception as e:
        print('--delete note error-- {}'.format(e))
        return HttpResponseNotFound()

    # 当用户id和文章id无法对应的时候返还404错误
    if uid != target_note.user.id:
        return HttpResponseNotFound()

    # 主任务逻辑
    # 伪删除 将note的is_active字段改为False
    target_note.is_active = False

    try:
        target_note.save()
    except Exception as e:
        print('--update note error-- {}'.format(e))
        return HttpResponse('删除笔记失败 原因：{}'.format(e))

    return HttpResponse('--delete note success!--')