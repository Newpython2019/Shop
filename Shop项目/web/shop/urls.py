from django.conf.urls import url
from . views import MemberViews,OrderViews,IndexViews

urlpatterns = [
#################### 网站首页 ####################
	# 商城首页url
    # url(r'^$', views.shop_homepage,name="shop_home"),
    url(r'^$', IndexViews.shop_homepage,name='shop_homepage'),
    # 商品列表
    url(r'^list/(?P<cid>[0-9]+)', IndexViews.shop_list,name='shop_list'),
    # 商品详情
    url(r'^info/$', IndexViews.shop_info,name='shop_info'),

#################### 前台登录 ####################
    # 登录页面
    url(r'^login/$', MemberViews.shop_login,name='shop_login'),
    # 登录验证
    url(r'^dologin/$', MemberViews.shop_dologin,name='shop_dologin'),
    # 退出登录
    url(r'^logout/$', MemberViews.shop_logout,name='shop_logout'),

    # 注册
    url(r'^register/$', MemberViews.shop_register,name='shop_register'),
    # 验证注册
    url(r'^doregister/$', MemberViews.shop_doregister,name='shop_doregister'),
    # 短信验证
    url(r'^sendMsg/$', MemberViews.shop_sendMsg,name='shop_sendMsg'),
    # 验证码
    url(r'^shop_code/$', MemberViews.shop_code,name='shop_code'),


    # 购物车 增删改查
    # 订单  确认订单，提交订单，订单支付
    # 个人中心  我的订单 个人信息 地址管理

###################### 其他 ######################

    # 精选品牌
    url(r'^SelectedBrands/$', OrderViews.shop_SelectedBrands,name='shop_SelectedBrands'),
    # 全球购
    url(r'^GlobalPurchase/$', OrderViews.shop_GlobalPurchase,name='shop_GlobalPurchase'),
    # 品牌馆
    url(r'^BrandPavilion/$', OrderViews.shop_BrandPavilion,name='shop_BrandPavilion'),

]