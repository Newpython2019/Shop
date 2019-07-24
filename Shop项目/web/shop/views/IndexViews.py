from django.shortcuts import render
from django.http import HttpResponse,Http404
from myadmin.models import Cates,Goods

# 商城首页视图
def shop_homepage(request):

	# 先获取一级分类
	OneTypeList = Cates.objects.filter(pid=0)
	for x in OneTypeList:
		# 再获取二级子类
		x.sub = Cates.objects.filter(pid=x.id)

	# 分配数据
	context = {'data':OneTypeList}

	# 加载商城首页视图
	return render(request,'myhome/homepage/homepage.html',context)

# 商品列表
def shop_list(request,cid):
	# 根据cid获取当前分类对象
	ob = Cates.objects.get(id=cid)
	# 判断当前是否为一级类
	if ob.pid == 0:
		# 获取当前一级类的所有子类
		ob.sub = Cates.objects.filter(id=ob.pid)
		# 获取当前二级分类下的所有商品
		goods = []
		for x in ob.sub:
			goods += x.goods_set.all().values()
		# 把当前分类下商品追加到数据中
		ob.goods = goods
		# 分配数据
		context = {'typelist':ob}
	else:
		# 获取当前分类的父级
		pob = Cates.objects.get(id=ob.pid)
		# 获取当前二级分类的同级分类
		pob.sub = Cates.objects.filter(pid=pob.id)
		for x in pob.sub:
			if x.id == ob.id:
				# 给当前的二级类加一个标识
				x.index = True

		# 获取当前类下的商品，不要同类的商品
		pob.goods = ob.goods_set.all()
		# 分配数据
		context = {'typelist':pob}

	return render(request,'myhome/homepage/list.html',context)

# 商品详情
def shop_info(request):
	try:
		# 根据商品id获取商品数据
		ob = Goods.objects.get(id=request.GET.get('goodsid'))
		# 分配数据
		context = {'goods':ob}
		

		# 加载模板
		return render(request,'myhome/homepage/info.html',context)
	except Exception as e:
		print('商品详情',e)
	raise Http404('您需要的页面找不到了...')