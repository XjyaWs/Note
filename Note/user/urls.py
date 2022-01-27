from django.urls import path
from . import views

urlpatterns = [

    # 登录界面
    path('login/', views.login_view, name='user_login'),
    # 登出
    path('logout/', views.logout_view, name='user_logout'),

    # 注册界面
    path('register/', views.register_view, name='user_register'),

    # 用户界面
    path('user_interface/', views.user_interface_view, name='user_interface'),

    # 修改密码界面
    path('change_password/', views.change_password, name='change_password'),

]
