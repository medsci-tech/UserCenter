from django.conf.urls import url
from admin.controller import admin,accounts, contract, mdset
urlpatterns = [
    url(r'^$', accounts.index, name='index'),
    url(r'^detail/$', admin.detail, name='detail'),
    url(r'^login/',accounts.login, name='login'),#登录
    url(r'^accounts/captcha', accounts.captcha,name='captcha'), #验证码
    url(r'^admin/list/',admin.list, name='list'),#管理员列表
    url(r'^contract/index', contract.index, name='contract'),
    url(r'^mdset/index', mdset.index, name='mdset'),
    #url(r'^logout/', admin.logout, name='logout'),
]
