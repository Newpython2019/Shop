from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse

from .. models import Cates
# Create your views here.

# 封装函数。格式化获取分类数据
def get_cates_all():
	# 获取所有分类
	# data = Cates.objects.all()

	# 解析SQL语句排序
	data = Cates.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

	# 处理数据的顺序,缩进,及父级名
	for x in data:
		l = x.path.count(',')-1
		x.sub = l*'| '
		# 添加父级名字
		if x.pid == 0:
			x.pname = '顶级分类'
		else:
			x.pname = Cates.objects.get(id=x.pid).name

	return data

# 分类 列表
def cate_index(request):
	# 获取数据
	data = get_cates_all()

	# 分配数据
	context = {'catelist':data}
	# 加载模板
	return render(request,'myadmin/cates/index.html',context)

# 分类 添加
def cate_add(request):
	if request.method == 'POST':
		# 接收数据
		data = {}
		data['name'] = request.POST.get('name')
		data['pid'] = request.POST.get('pid')

		# 判断是否为顶级分类
		if data['pid'] == '0':
			data['path'] = '0,'
		else:
			# 获取当前父级的path路径
			pob = Cates.objects.get(id=data['pid'])
			# 拼接当前数据的path
			data['path'] = pob.path+data['pid']+','
		# 数据入库
		ob = Cates(**data)
		ob.save()

		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_cate_index')+'"</script>')
		
	else:
		# 显示表单

		# 获取当前已有的分类
		catelist = get_cates_all()
		# 分配数据
		context = {'catelist':catelist}
		# 加载一个模板
		return render(request,'myadmin/cates/add.html',context)

# 分类 删除
def cate_del(request):

	cid = request.GET.get('cid')
	print(cid)
	# 判断当前分类下是否还有子类
	res = Cates.objects.filter(pid=cid).count()
	if res:
		# 有子类
		return JsonResponse({'msg':'当前类下有子类,不能删除','code':1})

	# 判断当前分类下是否还有商品


	# 接受cid，获取对象
	ob = Cates.objects.get(id=cid)
	# 执行删除
	ob.delete()
	return JsonResponse({'msg':'删除成功','code':0})

# 分类 名字修改
def cate_edit(request):
	try:
		# 获取 参数
		cid = request.GET.get('cid')
		newname = request.GET.get('newname')

		# 获取对象
		ob = Cates.objects.get(id=cid)
		ob.name = newname
		# 修改属性
		ob.save()
		data = {'msg':'更新成功','code':0}
	except:
		data = {'msg':'更新失败','code':1}
	# 返回结果
	return JsonResponse(data)
