from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from myadmin.models import Cates,Goods,Cart,Users,Order,OrderInfo

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

# ==================== 订单 ====================

# 订单列表
def shop_cart_confirm(request):

    # 获取选择的购物车id
    cartidstr = request.GET.get('cartids')
    cartids = cartidstr.split(',')

    # 把当前选择的购物车数据查询处理
    data = Cart.objects.filter(id__in=cartids)

    # 分配数据
    context = {'cartdata':data}

    return render(request, 'myhome/cart/confirm.html',context)

# 订单创建
def shop_cart_create(request):
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # 创建订单
    try:
        ob = Order()
        ob.uid = Users.objects.get(id=request.session.get('vipUser')['id'])
        ob.username = data['true_name']
        ob.phone = data['mob_phone']
        ob.address = data['address']
        ob.totalprice = 0
        ob.save()
    except Exception as e:
        print('创建订单',e)
        return HttpResponse("<script>alert('信息填写不正确');history.back(-1)</script>")

    # 创建订单详情
    try:
        cartdata = Cart.objects.filter(id__in = data['cartids0'].split(','))
        totalprice = 0
        for x in cartdata:
            obinfo = OrderInfo()
            obinfo.orderid = ob
            obinfo.goodsid = x.goodsid
            obinfo.num = x.num
            obinfo.save()
            # 计算总价
            totalprice += x.num*x.goodsid.price
            # 删除购物车中已经下单的商品
            x.delete()
        ob.totalprice = totalprice
        ob.save()
    except Exception as e:
        print('创建订单详情',e)
        return HttpResponse("<script>alert('订单有误');history.back(-1)</script>")

    # 重定向到支付页面
    return HttpResponse('<script>alert("订单创建成功,请支付");location.href="/cart/pay/?orderid='+str(ob.id)+'"</script>')

# 订单支付
def shop_cart_pay(request):
    orderid = request.GET.get('orderid')

    return HttpResponse('请支付您的订单-订单号为:'+str(orderid))