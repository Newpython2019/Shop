from django.shortcuts import render
from django.http import HttpResponse


# 商城首页视图
def shop_homepage(request):

	# 加载商城首页视图
	return render(request,'./myhome/shop_view/tpl/index.html')

