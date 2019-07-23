from django.shortcuts import render
from django.http import HttpResponse
from . CatesViews import get_cates_all
from .. models import Cates,Goods
from . UsersViews import uploads_pic
import os
from web.settings import BASE_DIR
# Create your views here.

# 商品添加 表单
def goods_add(request):
    # 获取当前所有的分类数据
    data = get_cates_all()
    # 分配数据
    context = {'catelist':data}

    # 显示一个添加的表单
    return render(request,'myadmin/goods/add.html',context)

# 商品 添加操作
def goods_insert(request):
	try:
		# 接收表单数据
		data = request.POST.dict()
		data.pop('csrfmiddlewaretoken')

		sku_price = request.POST.getlist('sku_price')
		sku_stock = request.POST.getlist('sku_stock')

		# 处理分类对象
		data['cateid'] = Cates.objects.get(id=data['cateid'])

		# 判断是否有图片的上传
		myfile = request.FILES.get('pic',None)
		if not myfile:
			return HttpResponse('<script>alert("必须上传图片");history.back(-1)</script>')
		# 处理 上传的文件
		data['pic_url'] = uploads_pic(myfile)

		# 执行添加
		ob = Goods(**data)
		ob.save()
		return HttpResponse('<script>alert("商品添加成功");location.href="/myadmin/goods/index";</script>')

	except Exception as e:
		print('商品添加',e)

	return HttpResponse('<script>alert("商品添加成功");history.back(-1)</script>')

# 商品列表
def goods_index(request):
    # 获取所有的商品对象
    data = Goods.objects.all()
    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分页类(每页显示几条)
    p = Paginator(data,5)
    # 获取当前页的数据
    pageindex = request.GET.get('page',1)
    userlist = p.page(pageindex)
    # 分配数据
    context = {'goodslist':data,'userlist':userlist}
    # 加载模板
    return render(request,'myadmin/goods/index.html',context)

# 商品编辑
def goods_edit(request):

    # 接受商品id
    cateid = request.GET.get('goodsid')
    # 获取当前用户对象
    ob = Goods.objects.get(id = cateid)
    # 获取当前所有的分类数据
    data = get_cates_all()

    # 判断当前的请求方式
    if request.method == 'POST':
        # 判断所属分类是否更新
        if request.POST.get('cateid'):
            ob.cateid_id = request.POST.get('cateid')
        # 判断头像是否更新
        try:
            myfile = request.FILES.get('pic',None)
            if myfile:
                # 如果有新头像上传，则先删除原头像图片
                if ob.pic_url:
                    os.remove(BASE_DIR+ob.pic_url)
                # 再上传新的头像
                ob.pic_url = uploads_pic(myfile)
        except Exception as e:
            print('头像更新操作',e)

        # 更新其它字段
        try:
            ob.goodsname = request.POST.get('goodsname')
            ob.title = request.POST.get('title')
            ob.price = request.POST.get('price')
            ob.goodsnum = request.POST.get('goodsnum')
            if request.POST.get('goodsinfo'):
                ob.goodsinfo = request.POST.get('goodsinfo')
            ob.save()
        except Exception as e:
            print('字段更新操作',e)
        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/goods/index/";</script>')

    else:
        # 显示编辑表单
        context = {'uinfo':ob,'catelist':data}
        return render(request,'myadmin/goods/edit.html',context)


