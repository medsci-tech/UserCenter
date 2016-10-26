from django.conf.urls import url
from admin.controller import (
    admin,
    accounts,
    contract,
    upload,
    app,
    credit_rule,
    syslog,
    company,
    credit_config,
    user,
    charts,
)

urlpatterns = [
    # 登录
    url(r'^$', accounts.index, name='index'),
    url(r'^login/',accounts.login, name='accounts_login'),# 登录
    url(r'^logout/', accounts.logout, name='accounts_logout'),  # 注销退出
    url(r'^accounts/captcha', accounts.captcha,name='accounts_captcha'), # 验证码

    # 管理员
    url(r'^detail/$', admin.detail, name='admin_detail'),
    url(r'^admin/updateStatus/',admin.updateStatus, name='admin_updateStatus'),
    url(r'^admin/list/',admin.list, name='admin'),# 管理员列表
    url(r'^admin/save/',admin.save, name='save'),# 保存管理员

    # 合同
    url(r'^contract/contractlist', contract.contractlist, name='contract_contractlist'),# 保存合同
    url(r'^contract/delete', contract.delete, name='contract_delete'),# 保存合同
    url(r'^contract/save', contract.save, name='contract_save'),# 保存合同
    url(r'^contract/updateStatus', contract.updateStatus, name='contract_updateStatus'),
    url(r'^contract/credit', contract.credit, name='contract_credit'),
    url(r'^contract/index', contract.index, name='contract'), # 合同列表

    # 文件上传
    url(r'^upload/img', upload.img, name='upload_img'),

    # 应用平台
    url(r'^app/delete', app.delete, name='app_delete'),
    url(r'^app/form', app.form, name='app_form'),
    url(r'^app/stats', app.stats, name='app_stats'),
    url(r'^app/applist', app.applist, name='app_applist'),
    url(r'^app/index', app.index, name='app'),

    # 积分策略配置
    url(r'^credit_rule/form', credit_rule.form, name='credit_rule_form'),
    url(r'^credit_rule/stats', credit_rule.stats, name='credit_rule_stats'),
    url(r'^credit_rule/index', credit_rule.index, name='credit_rule'),

    # 系统操作日志
    url(r'^logs/index', syslog.index, name='logs'),

    # 企业管理
    url(r'^company/delete', company.delete, name='company_delete'),
    url(r'^company/form', company.form, name='company_form'),
    url(r'^company/stats', company.stats, name='company_stats'),
    url(r'^company/index', company.index, name='company'),

    # 迈豆池管理
    url(r'^credit_config/creditconfiglist', credit_config.creditconfiglist, name='credit_config_creditconfiglist'),
    url(r'^credit_config/form', credit_config.form, name='credit_config_form'),
    url(r'^credit_config/stats', credit_config.stats, name='credit_config_stats'),
    url(r'^credit_config/index', credit_config.index, name='credit_config'),

    # 用户管理
    url(r'^user/form', user.form, name='user_form'),
    url(r'^user/stats', user.stats, name='user_stats'),
    url(r'^user/index', user.index, name='user'),

    # 图表
    url(r'^charts/index', charts.index, name='charts'),

]
