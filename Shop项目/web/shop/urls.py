from django.conf.urls import url
from . import views

urlpatterns = [
	# 商城首页url
    url(r'^$', views.shop_homepage,name='shop_homepage'),
    # 列表
    url(r'^list/$', views.shop_list,name='shop_list'),
    # url(r'^list1/$', views.shop_list1,name='shop_list1'),

    # 详情
    # url(r'^info/$', views.shop_info,name='shop_info'),

    # 登录
    url(r'^login/$', views.shop_login,name='shop_login'),
    url(r'^dologin/$', views.shop_dologin,name='shop_dologin'),
    url(r'^logout/$', views.shop_logout,name='shop_logout'),

    # 注册
    url(r'^register/$', views.shop_register,name='shop_register'),
    url(r'^doregister/$', views.shop_doregister,name='shop_doregister'),
    # 验证码
    url(r'^code/$', views.shop_code,name='shop_code'),
    # url(r'^codeValid/$', views.shop_codeValid,name='shop_codeValid'),
    
    

    # 购物车 增删改查
    # 订单  确认订单，提交订单，订单支付
    # 个人中心  我的订单 个人信息 地址管理
]