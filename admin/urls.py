from django.conf.urls import url
from admin.controller import admin,accounts
urlpatterns = [
    url(r'^$', accounts.index, name='index'),
    url(r'^detail/$', admin.detail, name='detail'),
    url(r'^login/',accounts.login, name='login'),#登录
    url(r'^accounts/captcha', accounts.captcha,name='captcha'), #验证码
    url(r'^list/',admin.list, name='list'),#管理员列表
    #url(r'^logout/', admin.logout, name='logout'),
]