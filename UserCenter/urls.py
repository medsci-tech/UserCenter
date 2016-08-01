from django.conf.urls import *
from users import temp
urlpatterns = patterns(
    url(r'^/$', temp.index),
    url(r'^temp/index', temp.index),
    url(r'^temp/calendar', temp.calendar),
    url(r'^temp/tables', temp.tables),
    url(r'^temp/', temp.index),
)
