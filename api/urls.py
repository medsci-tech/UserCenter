from django.conf.urls import url
from api.controller import (
    login,
)

urlpatterns = [
    # 用户登录
    url(r'^login/test', login.test, name='login_test'),
    url(r'^login/wechat', login.wechat, name='login_wechat'),
    url(r'^login/user_pwd', login.user_pwd, name='login_userPwd'),
]
