from django.conf.urls import *
from users import temp,tests
urlpatterns = patterns(
    url(r'^temp/index', temp.index),
    url(r'^temp/tables', temp.tables),
    url(r'^temp/testdb', temp.testdb),
    url(r'^temp/', temp.index),

    url(r'', temp.login),
)
