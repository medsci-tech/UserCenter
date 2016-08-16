from django.conf.urls import url
from admin.controller import admin
urlpatterns = [
    #url(r'^$', login.index, name='index'),
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^login/', admin.login, name='login'),#登录
]
