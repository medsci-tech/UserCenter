from django.conf.urls import *
from users.controller import manager
from users import temp, tests  # test
urlpatterns = patterns(

    url(r'^manager/list', manager.index),
    url(r'^manager', manager.index),

    # test
    url(r'^temp/index', temp.index),
    url(r'^temp/tables', temp.tables),
    # url(r'^temp/testdb', temp.testdb),
    # url(r'^temp/', temp.index),
    url(r'', temp.login),
)
