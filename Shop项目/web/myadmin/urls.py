from django.conf.urls import url
from . views import IndexViews,UsersViews

urlpatterns = [
	# 后台主界面
    url(r'^$',IndexViews.index,name="myadmin_index"),
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

]
