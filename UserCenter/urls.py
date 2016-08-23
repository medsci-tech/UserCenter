from django.conf.urls import *
from users.controller import admin, contract
urlpatterns = (

    # 管理员管理
    url(r'^admin/form', admin.form),
    url(r'^admin/stats', admin.stats),
    url(r'^admin/', admin.index),
    # 合同信息管理
    url(r'^contract/form', contract.form),
    url(r'^contract/stats', contract.stats),
    url(r'^contract/', contract.index),

)
