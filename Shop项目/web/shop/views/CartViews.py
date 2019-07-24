from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from myadmin.models import Cates,Goods,Cart,Users

# ==================== 购物车 ====================

# 添加
def shop_cart_add(request):
    try:
        # 执行购物车的商品添加
        data = request.GET.dict()
        data['goodsid'] = Goods.objects.get(id=data['goodsid'])
        data['uid'] = Users.objects.get(id=request.session.get('vipUser')['id'])
        # 先检测当前的商品是否已经在当前用户的购物车中
        ob = Cart.objects.filter(uid=data['uid']).filter(goodsid=data['goodsid'])

        if ob.count():
            # 存在 获取当前购物车对象
            cart = Cart.objects.get(id=ob[0].id)
            cart.num += int(data['num'])
            cart.save()
        else:
            # 不存在
            # 存入cart模型中
            ob = Cart(**data)
            ob.save()
        return JsonResponse({'code': 0, 'msg': '加入购物车成功'})
    except Exception as e:
        print('执行购物车的商品添加', e)
    return JsonResponse({'code': 1, 'msg': '加入购物车失败'})


# 列表
def shop_cart_index(request):
    # 获取当前用户的购物车数据
    vipUser = request.session.get('vipUser')
    data = Cart.objects.filter(uid=vipUser['id'])
    # 分配数据
    context = {'cartdata': data}

    # 加载模板
    return render(request, 'myhome/cart/index.html', context)


# 删除
def shop_cart_del(request):
    try:
        cartid = request.GET.get('cartid')
        print(cartid)
        # 获取当前购物车商品对象
        ob = Cart.objects.get(id=cartid)
        # 执行删除
        ob.delete()
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        print('购物车删除', e)
    return JsonResponse({'code': 1, 'msg': '删除失败'})

# 清空
def shop_cart_clear(request):
    return HttpResponse('a')


# 编辑
def shop_cart_edit(request):
	try:
		cartid = request.GET.get('cartid')
		num = request.GET.get('num')
		# 根据id获取购物车对象
		ob = Cart.objects.get(id=cartid)
		ob.num = num
		ob.save()
		return JsonResponse({'code': 0, 'msg': '编辑成功'})
	except Exception as e:
		print('商品数量编辑',e)
	return JsonResponse({'code': 1, 'msg': '编辑失败'})