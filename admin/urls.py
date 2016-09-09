from django.conf.urls import url
from admin.controller import admin,accounts, contract, mdset, upload, app, credit, credit_rule

urlpatterns = [
    # 登录
    url(r'^$', accounts.index, name='index'),
    url(r'^login/',accounts.login, name='accounts_login'),# 登录
    url(r'^accounts/captcha', accounts.captcha,name='accounts_captcha'), # 验证码

    # 管理员
    url(r'^detail/$', admin.detail, name='admin_detail'),
    url(r'^admin/stats/',admin.stats, name='admin_stats'),
    url(r'^admin/list/',admin.list, name='admin'),# 管理员列表
    url(r'^admin/save/',admin.save, name='save'),# 保存管理员

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
    url(r'^credit/form', credit.form, name='credit_form'),
    url(r'^credit/stats', credit.stats, name='credit_stats'),
    url(r'^credit/index', credit.index, name='credit'),

    # 积分策略配置
    url(r'^credit_rule/form', credit_rule.form, name='credit_rule_form'),
    url(r'^credit_rule/stats', credit_rule.stats, name='credit_rule_stats'),
    url(r'^credit_rule/index', credit_rule.index, name='credit_rule'),
]
