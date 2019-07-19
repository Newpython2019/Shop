from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from myadmin.models import Users
#引入绘图模块
from PIL import Image, ImageDraw, ImageFont
#引入随机函数模块
import random
import io


# 商城首页视图
def shop_homepage(request):

	# 加载商城首页视图
	return render(request,'myhome/shop_view/tpl/index.html')

# 列表
def shop_list(request):

	return render(request,'myhome/shop_view/tpl/list.html')

# 商品详情
# def shop_info(request):

	# return render(request,'myhome/shop_view/tpl/')

# 显示登录页面
def shop_login(request):

	return render(request,'myhome/shop_view/tpl/login.html')

# 执行登录
def shop_dologin(request):
	try:
		# 验证手机号码，判断用户是否存在
		ob = Users.objects.get(phone=request.POST['phone'])
		# 验证密码
		pw = Users.objects.get(password=request.POST['password'])

		# 验证验证码
		vc = request.POST['code']
		print(vc)
		if vc.upper() != request.session['verifycode']:
			return HttpResponse('<script>alert("验证码有误");location.href="/shop/login/"</script>')

		if pw:
			# 验证成功
			request.session['vipUser'] = {
			'id':ob.id,'phone':ob.phone,'password':ob.password,'pic_url':ob.pic_url
			}
			return HttpResponse('<script>alert("登录成功");location.href="/shop"</script>')

		

	except:
		pass

	return HttpResponse('<script>alert("手机号或密码不正确");location.href="/shop/login"</script>')

# 退出登录
def shop_logout(request):
	del request.session['vipUser']
	return HttpResponse('<script>alert("退出成功");location.href="/shop"</script>')


# 显示注册页面
def shop_register(request):

	return render(request,'myhome/shop_view/tpl/register.html')

# 执行注册
def shop_doregister(request):
	try:
		# 接收表单数据
		data = request.POST.dict()

		# 暂时不存
		data.pop('csrfmiddlewaretoken')
		data.pop('mobile_code')
		data.pop('password_confirm')
		data.pop('agree')
		
		# 验证手机号是否存在
		res = Users.objects.filter(phone=data['phone']).count()
		if res:
			# 手机号已经存在
			return HttpResponse('<script>alert("手机号已存在");history.back(-1)</script>')


		# 验证验证码
		if data['code'].upper() != request.session['verifycode']:
			return HttpResponse('<script>alert("验证码有误");location.href="/shop/register/"</script>')
		data.pop('code')		

		# 密码进行加密处理
		

		# 执行注册  数据的添加
		obj = Users(**data)
		obj.save()
		return HttpResponse('<script>alert("注册成功，请登录");location.href="/shop/login/"</script>')

	except:
		pass

	return HttpResponse('<script>alert("注册失败，请联系管理员");location.href="/shop/register/"</script>')


# 验证码
def shop_code(request):
    
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 40
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('Inkfree.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


