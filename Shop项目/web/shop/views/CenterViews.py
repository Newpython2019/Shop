from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from myadmin.models import Cates,Goods,Cart,Users,Order,OrderInfo


# ==================== 个人中心 ====================

# 个人订单
def shop_center_order(request):

	# 获取当前用户的所有订单
	orderdata = Order.objects.filter(uid=request.session.get('vipUser')['id'])

	# 分配数据
	context = {'orderdata':orderdata}

	# 加载模板
	return render(request,'myhome/member/order.html',context)
	