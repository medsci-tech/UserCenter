from django.conf.urls import url
from api.controller import (
    public,
    user,
    credit,
    beans_chart,
)
from api import tests

urlpatterns = [

    # 测试
    url(r'^tests/index', tests.index, name='public_get_token'),

    # 公共访问
    url(r'^public/get_token', public.get_token, name='public_get_token'),
    url(r'^public/login', public.login, name='public_login'),
    url(r'^public/register', public.register, name='public_register'),
    url(r'^public/setPwd', public.setPwd, name='public_setPwd'),

    # 积分图表
    url(r'^beans_chart/project_type', beans_chart.project_type, name='beans_chart_project_type'),
    url(r'^beans_chart/type_rule', beans_chart.type_rule, name='beans_chart_type_rule'),
    url(r'^beans_chart/rule_time', beans_chart.rule_time, name='beans_chart_rule_time'),

    # 用户信息修改
    url(r'^user/edit', user.edit, name='user_edit'),

    # 迈豆积分接口
    url(r'^credit/index', credit.index, name='credit_index'),
    url(r'^credit/query', credit.query, name='credit_query'),
]
