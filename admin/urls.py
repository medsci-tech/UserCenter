from django.conf.urls import url
from admin.controller import admin,accounts, contract, mdset, upload
urlpatterns = [
    url(r'^$', accounts.index, name='index'),
    url(r'^detail/$', admin.detail, name='detail'),
    url(r'^login/',accounts.login, name='login'),#登录
    url(r'^accounts/captcha', accounts.captcha,name='captcha'), #验证码
    url(r'^admin/list/',admin.list, name='list'),#管理员列表
    url(r'^contract/index', contract.index, name='contract'),
    url(r'^contract/test', contract.test, name='contract_test'),

    # 迈豆积分设置
    url(r'^mdset/form', mdset.form, name='mdset_form'),
    url(r'^mdset/stats', mdset.stats, name='mdset_stats'),
    url(r'^mdset/index', mdset.index, name='mdset'),

    # 文件上传
    url(r'^upload/img', upload.img, name='upload_img'),
]
