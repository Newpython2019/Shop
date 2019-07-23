from django import template
from myadmin.models import Cates
register = template.Library()

from django.utils.html import format_html
from django.core.urlresolvers import reverse

# 自定义模板导航标签
@register.simple_tag
def showNav():
	# 获取一级分类
	Cateslist = Cates.objects.filter(pid=0)
	s = ''
	for x in Cateslist:
		s += '''
		<li>
			<a href="{url}">{name}</a>
		</li>
		'''.format(name=x.name,url=reverse('shop_list',args=(x.id,)))
	return format_html(s)

# 自定义分页标签
@register.simple_tag
def showpage(count,request):

	try:
		# 接收当前页码数
		p = int(request.GET.get('page',1))

		# 获取当前请求中所有参数
		data = request.GET.dict()
		args = ''
		# 循环关键参数并拼接
		for k,v in data.items():
			print(k,v)
			if k!='page':
				args += '&'+k+'='+v

		start = p-5
		end = p+4

		# 判断 如果当前页 小于5
		if p<= 5:
			start = 1
			end = 10
		# 判断 如果当前页 大于 总页数-5
		if p > count-5:
			start = count-9
			end = count
		# 判断 如果总页数 小于10
		if count < 10:
			start = 1
			end = count

		pagehtml = ''
		# 首页
		pagehtml += '<li><a href="?page=1{args}">首页</a></li>'.format(args=args)
		# 上一页
		if p > 1:
			pagehtml += '<li><a href="?page={p}{args}">上一页</a></li>'.format(p=p-1,args=args)
		# 数字页码
		for x in range(start,end+1):
			# 判断是否为当前页-高亮显示
			if p == x:
				pagehtml += '<li class="am-active"><a href="?page={p}{args}">{p}</a></li>'.format(p=x,args=args)
			else:
				pagehtml += '<li><a href="?page={p}{args}">{p}</a></li>'.format(p=x,args=args)

		# 下一页
		if p < count:
			pagehtml += '<li><a href="?page={p}{args}">下一页</a></li>'.format(p=p+1,args=args)

		# 尾页
		pagehtml += '<li><a href="?page={p}{args}">尾页</a></li>'.format(p=count,args=args)

		# 格式化html
		return format_html(pagehtml)
		# return pagehtml
	except Exception as e:
		print('分页标签',e)
	