from django.conf.urls import url
from api.controller import (
    public,
)

urlpatterns = [

    # 公共访问
    url(r'^public/get_token', public.get_token, name='public_get_token'),
    url(r'^public/login', public.login, name='public_login'),
    url(r'^public/register', public.register, name='public_register'),

    # 用户注册
]
