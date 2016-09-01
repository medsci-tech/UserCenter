from django.conf.urls import url
from admin.controller import admin,accounts, contract, mdset, upload
urlpatterns = [
    # 登录
    url(r'^$', accounts.index, name='index'),
    url(r'^login/',accounts.login, name='accounts_login'),#登录
    url(r'^accounts/captcha', accounts.captcha,name='accounts_captcha'), #验证码

    # 管理员
    url(r'^detail/$', admin.detail, name='admin_detail'),
    url(r'^admin/form/',admin.form, name='admin_form'),
    url(r'^admin/stats/',admin.stats, name='admin_stats'),
    url(r'^admin/list/',admin.list, name='admin'),#管理员列表

    # 合同
    url(r'^contract/form', contract.form, name='contract_form'),
    url(r'^contract/stats', contract.stats, name='contract_stats'),
    url(r'^contract/index', contract.index, name='contract'),

    # 迈豆积分设置
    url(r'^mdset/form', mdset.form, name='mdset_form'),
    url(r'^mdset/stats', mdset.stats, name='mdset_stats'),
    url(r'^mdset/index', mdset.index, name='mdset'),

    # 文件上传
    url(r'^upload/img', upload.img, name='upload_img'),
]
