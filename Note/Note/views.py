from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpRequest


def index_view(request: HttpRequest):

    login_flag = False
    user_name = request.session.get("user_name")

    # 判断用户是否登录
    if user_name:
        login_flag = True
    else:
        user_name = request.COOKIES.get("user_name")
        if user_name:
            login_flag = True
            uid = request.COOKIES.get("uid")

            # 重新录入session中
            request.session["user_name"] = user_name
            request.session["uid"] = uid
        else:
            user_name = ''

    return render(request, 'index.html', locals())


def blank_view(request):
    return HttpResponseRedirect(reverse('index'))