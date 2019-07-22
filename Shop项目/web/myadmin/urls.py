from django.conf.urls import url
from . views import IndexViews,UsersViews,CatesViews,GoodsViews

urlpatterns = [
	# 后台主界面跳转
    url(r'^$',IndexViews.index,name="myadmin_index"),

    # 登录页
    url(r'^login/$',IndexViews.myadmin_login,name="myadmin_login"),
    # 登录处理
    url(r'^dologin/$',IndexViews.myadmin_dologin,name="myadmin_dologin"),
    # 验证码
    url(r'^verifycode/$',IndexViews.verifycode,name="myadmin_vcode"),
    # 退出
    url(r'^logout/$',IndexViews.myadmin_logout,name="myadmin_logout"),

    # 用户管理
    # 用户添加列表
    url(r'^user/add/$',UsersViews.user_add,name="myadmin_user_add"),
    # 用户列表数据添加
    url(r'^user/insert/$',UsersViews.user_insert,name="myadmin_user_insert"),
    # 用户列表数据
    url(r'^user/index/$',UsersViews.user_index,name="myadmin_user_index"),
    # 用户数据编辑
    url(r'^user/edit/$',UsersViews.user_edit,name="myadmin_user_edit"),
    # 用户状态设置
    url(r'^user/setstatus/$',UsersViews.user_set_status,name="myadmin_user_set_status"),


    # 分类管理
    # 商品分类添加
    url(r'^cate/add/$',CatesViews.cate_add,name="myadmin_cate_add"),
    # 商品分类列表
    url(r'^cate/index/$',CatesViews.cate_index,name="myadmin_cate_index"),
    # 商品分类删除
    url(r'^cate/del/$',CatesViews.cate_del,name="myadmin_cate_del"),
    # 商品分类删除
    url(r'^cate/edit/$',CatesViews.cate_edit,name="myadmin_cate_edit"),

    # 商品管理
    # 商品添加页
    url(r'^goods/add/$',GoodsViews.goods_add,name="myadmin_goods_add"),
    # 商品添加
    url(r'^goods/insert/$',GoodsViews.goods_insert,name="myadmin_goods_insert"),
    # 商品列表页
    url(r'^goods/index/$',GoodsViews.goods_index,name="myadmin_goods_index"),
    # 用户数据编辑
    url(r'^goods/edit/$',GoodsViews.goods_edit,name="myadmin_goods_edit"),


]