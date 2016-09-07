from django.conf.urls import url
from admin.controller import admin,accounts, contract, mdset, upload, app, system, tactics

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

    # 迈豆兑换
    url(r'^mdset/form', mdset.form, name='mdset_form'),
    url(r'^mdset/stats', mdset.stats, name='mdset_stats'),
    url(r'^mdset/index', mdset.index, name='mdset'),

    # 文件上传
    url(r'^upload/img', upload.img, name='upload_img'),

    # 应用平台
    url(r'^app/form', app.form, name='app_form'),
    url(r'^app/stats', app.stats, name='app_stats'),
    url(r'^app/applist', app.applist, name='app_applist'),
    url(r'^app/index', app.index, name='app'),

    # 积分基础配置
    url(r'^system/form', system.form, name='system_form'),
    url(r'^system/stats', system.stats, name='system_stats'),
    url(r'^system/index', system.index, name='system'),

    # 积分策略配置
    url(r'^tactics/form', tactics.form, name='tactics_form'),
    url(r'^tactics/stats', tactics.stats, name='tactics_stats'),
    url(r'^tactics/index', tactics.index, name='tactics'),
]
