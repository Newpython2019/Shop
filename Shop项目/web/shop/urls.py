from django.conf.urls import url
from . import views

urlpatterns = [
	# 商城首页url
     url(r'^$', views.shop_homepage,name="shop_home"),
]