from django.conf.urls import *
from users.controller import admin
from users import temp, tests  # test
urlpatterns = (

    # 管理员管理
    url(r'^admin/form', admin.form),
    url(r'^admin/stats', admin.stats),
    url(r'^admin/', admin.index),
    # test
    url(r'^temp/index', temp.index),
    url(r'^temp/tables', temp.tables),
    # url(r'^temp/testdb', temp.testdb),
    # url(r'^temp/', temp.index),
    # url(r'', temp.login),
)
