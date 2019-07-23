############### 用户模块 ###############
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse,Http404
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render
from myadmin.models import Users
import random
import os
import io

# ==================== 登录 ====================

# 显示登录页面
def shop_login(request):

	return render(request,'myhome/member/login.html')

# 执行登录
def shop_dologin(request):
	try:
		# 验证手机号码，判断用户是否存在
		ob = Users.objects.get(phone=request.POST['phone'])
		# 验证密码
		pw = check_password(request.POST['password'],ob.password)
		# 验证验证码
		vc = request.POST['code']
		# print(vc)
		if vc.upper() != request.session['verifycode']:
			return HttpResponse('<script>alert("验证码有误");history.back(-1);</script>')
		if pw:
			# 验证成功
			request.session['vipUser'] = {
			'id':ob.id,'phone':ob.phone,'password':ob.password,'pic_url':ob.pic_url,'nikename':ob.nikename
			}
			return HttpResponse('<script>alert("登录成功");location.href="/shop"</script>')
	except Exception as e:
		print('账号密码验证',e)

	return HttpResponse('<script>alert("手机号或密码不正确");history.back(-1);</script>')

# 退出登录
def shop_logout(request):
	del request.session['vipUser']
	return HttpResponse('<script>alert("退出成功");location.href="/shop"</script>')

# ==================== 注册 ====================

# 显示注册页面
def shop_register(request):

	return render(request,'myhome/member/register.html')

# 执行注册
def shop_doregister(request):
	try:
		# 接收表单数据
		data = request.POST.dict()
		print(data)
		# 暂时不存
		data.pop('csrfmiddlewaretoken')
		pwd2 = data.pop('password_confirm')
		data.pop('agree')

		# 验证手机短信验证码是否正确
		if data['vcode'] != request.session['msgcode']:
			return HttpResponse('<script>alert("手机验证码错误");history.back(-1)</script>')
		# 删除表单中的 vcode
		data.pop('vcode')

		# 判断是否为空
		if data['nikename'] == '' or data['phone'] == '' or data['password'] == '':
			return HttpResponse('<script>alert("请正确填写信息");history.back(-1)</script>')
		# 判断密码是否一致
		if data['password'] != pwd2:
			data['nikename'] == ''
			data['phone'] == ''
			return HttpResponse('<script>alert("密码不一致");history.back(-1)</script>')
		# 验证手机号是否存在
		res = Users.objects.filter(phone=data['phone']).count()
		if res:
			# 手机号已经存在
			return HttpResponse('<script>alert("手机号已存在");history.back(-1)</script>')

		# 密码进行加密处理
		data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')
		

		# 执行注册  数据的添加
		obj = Users(**data)
		obj.save()
		return HttpResponse('<script>alert("注册成功，请登录");location.href="/shop/login/"</script>')

	except Exception as e:
		print('执行注册',e)

	return HttpResponse('<script>alert("注册失败，请联系管理员");location.href="/shop/register/"</script>')

# ==================== 验证 ====================

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

# 短信验证
def shop_sendMsg(request):
	import random
	# 接收手机号码
	phone = request.GET.get('phone')
	print(phone)
	# 随机验证码
	code = str(random.randint(10000,99999))
	# 把验证码存入session
	request.session['msgcode'] = code
	# 调用方法,发送短信验证
	res = hywx_send(phone,code)
	return JsonResponse(res)

# 短信接口
def hywx_send(mobile,code):
	#接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
    #账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
    #注意事项：
    #（1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
    #（2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
    #（3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；
      
    # import urllib2
    import urllib
    import urllib.request
    import json
 
    #用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account  = "C46788523" 
    #密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "0b838daf6a961f9c568c1cad56c3ab98"
    # mobile = request.GET.get('phone')
  
    text = "您的验证码是："+code+"。请不要把验证码泄露给其他人。"
    data = {'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' }
    # req = urllib.request.urlopen(
    #     url= 'http://106.ihuyi.com/webservice/sms.php?method=Submit',
    #     data= urllib.parse.urlencode(data).encode('utf-8')
    # )
    # 获取接口响应的内容
    # content = req.read()
    # res = json.loads(content.decode('utf-8'))
    # 15637004571738806283

    res = {'code':2,'msg':'提交成功','id':'15637004571738806283','yzm':code}
    return res