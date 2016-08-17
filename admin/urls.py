from django.conf.urls import url
from admin.controller import admin,accounts
urlpatterns = [
    url(r'^$', admin.index, name='index'),
    #url(r'^(?P<q_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^login/',admin.login, name='login'),#登录
    url(r'^accounts/', accounts.captcha,name='captcha'), #验证码
    #url(r'^logout/', admin.logout, name='logout'),
]
